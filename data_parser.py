from __future__ import annotations

from abc import ABC, abstractmethod

import lark
from lark import Lark
from lark.visitors import Interpreter, v_args
from argparse import ArgumentParser
import struct
import pathlib

grammar = r"""
start: top_level*

?top_level: struct | templated_struct | enum

template: "template" "<" _template_param_list ">"
_template_param_list: ((template_param ",")* template_param)?
?template_param: "typename" IDENTIFIER -> template_param_type
            | type IDENTIFIER -> template_param_const
templated_struct: template "struct" IDENTIFIER struct_items ";"
struct: "struct" IDENTIFIER struct_items ";"

struct_items: "{" struct_item* "}"
struct_item: decl ("=" const_expr)? ";" -> field
           | IDENTIFIER parenthesized initializer_list block -> constructor
           | type IDENTIFIER parenthesized block -> method

decl: type IDENTIFIER ("[" const_expr "]")*

initializer_list: (":" (initializer ",")* initializer)?
initializer: IDENTIFIER parenthesized

?const_expr: number
           | IDENTIFIER -> ident

enum: "enum" "class"? IDENTIFIER "{" _enum_variants "}" ";"
_enum_variants: (enum_variant ("," enum_variant)*)?
enum_variant: IDENTIFIER

?inner: bracketed | parenthesized | block | TOKEN | ";"
bracketed: "[" inner* "]"
parenthesized: "(" inner* ")"
block: "{" inner* "}"

?type: IDENTIFIER -> type_name
     | IDENTIFIER "<" template_args ">" -> type_generic
template_args: (template_arg ("," template_arg)*)?
?template_arg: type | const_expr

%import common.ESCAPED_STRING -> STRING
IDENTIFIER: /[a-zA-Z_][a-zA-Z_0-9]*/

DECIMAL: /[0-9]+/
BINARY: /0b[0-9]+/
HEX: /0x[0-9]+/
OCT: /0o[0-9]+/

number: DECIMAL | BINARY | HEX | OCT

TOKEN: IDENTIFIER
     | STRING
     | DECIMAL | BINARY | HEX | OCT
     | "." | "," | "?" | "/" | "=" | "+"
     | "-" | "*" | "~" | "!" | "%" | "^"
     | "&" | "|" | ":" | "<" | ">" 

%import common.C_COMMENT
%import common.CPP_COMMENT
%import common.WS
%ignore C_COMMENT
%ignore CPP_COMMENT
%ignore WS
"""


class Type(ABC):
    """
    An abstract class which represents Types in C++. As such, it stores a size and alignment, which is all we
    care about. Furthermore, it requires that deriving classes implement a "parse" method, which must extract
    information from the bytes representing this types into json.
    """
    def __init__(self, size: int, align: int):
        self.size = size
        self.align = align

    @staticmethod
    def _calc(types: list[Type]) -> tuple[int, int]:
        """
        Given a list of types, return the total size and the required alignment for that sequence of types.

        Total size is more than just the sum of sizes of the types, since we must account for alignment requirements.
        Required alignment is just the alignment of the most aligned element in the types.

        :param types: A list of Type instances
        :return: A tuple of (total size, required alignment)
        """
        idx = 0
        max_align = 1
        for typ in types:
            size, align = typ.size, typ.align
            if idx % align != 0:
                idx += align - idx % align
            idx += size
            if align > max_align:
                max_align = align
        return idx, max_align

    @staticmethod
    def _get_parts(data: bytes, types: list[Type]) -> list[bytes]:
        """
        Given some bytes and a list of types that the bytes represent, yield a list of bytes, each of which corresponds
        to a type in the list of types. This function takes into account padding bytes used for alignment and ignores them.

        :param data: Some bytes, which must be exactly as large as the size used to represent `types`
        :param types: A list of types, whose data is stored by `data`
        :return: A list of bytes, which correspond to ranges in `data` for each type in `types`
        """
        idx = 0
        parts = []
        for typ in types:
            size, align = typ.size, typ.align
            if idx % align != 0:
                idx += align - idx % align
            parts.append(data[idx:idx+size])
            idx += size
        return parts

    @abstractmethod
    def parse(self, data: bytes): ...

    def __repr__(self):
        return f"{self.__class__.__name__}(size={self.size}, align={self.align})"


class Struct(Type):
    def __init__(self, members: dict[str, Type]):
        self.members = members
        size, align = self._calc(list(self.members.values()))
        super().__init__(size, align)

    def parse(self, data: bytes):
        parsed = {}
        parts = self._get_parts(data, list(self.members.values()))
        for (name, typ), part in zip(self.members.items(), parts):
            parsed[name] = typ.parse(part)
        return parsed


class Array(Type):
    def __init__(self, item: Type, count: int):
        self.item = item
        self.count = count
        size, align = self._calc([item]*count)
        super().__init__(size, align)

    def parse(self, data: bytes):
        parsed = [self.item.parse(item) for item in self._get_parts(data, [self.item]*self.count)]
        return parsed


class Enum(Type):
    def __init__(self, variants: dict[int, str]):
        self.variants = variants
        super().__init__(4, 4)

    def parse(self, data: bytes):
        as_int = struct.unpack("i", data)[0]
        return self.variants[as_int]


class Boolean(Type):
    def __init__(self):
        super().__init__(1, 1)

    def parse(self, data: bytes):
        return struct.unpack("?", data)[0]


class Integer(Type):
    def __init__(self, size: int, signed: bool = True, align: int = None):
        super().__init__(size, size if align is None else align)
        if size == 1 and signed:
            self._format = "b"
        elif size == 1 and not signed:
            self._format = "B"
        elif size == 2 and signed:
            self._format = "h"
        elif size == 2 and not signed:
            self._format = "H"
        elif size == 4 and signed:
            self._format = "i"
        elif size == 4 and not signed:
            self._format = "I"
        else:
            raise Exception(size, signed)

    def parse(self, data: bytes):
        return struct.unpack(self._format, data)[0]


class Float(Type):
    def __init__(self, size: int, align: int = None):
        super().__init__(size, size if align is None else align)
        if size == 4:
            self._format = "f"
        elif size == 8:
            self._format = "d"
        else:
            raise Exception()

    def parse(self, data: bytes):
        return struct.unpack(self._format, data)[0]


class Template:
    """
    Generated whenever a templated struct is encountered. It stores what template parameters it requires (what type and
    what name they have), as well as the Context it was in and the fields of the struct (as AST).
    """
    def __init__(self, params: list[tuple[str, str]], fields: list[lark.Tree], ctxt: Context):
        """
        :param params: A list of parameter info tuples. The first item of the tuple should be either the string
        "typename" if it expects a type, or anything else otherwise. The second item of the tuple should be the name the
        parameter has. So template<typename T> would have a params of [("typename, "T")]
        :param fields: The fields of the templated struct, preserved in their AST node form. This makes substitution of
        template parameters really simple. The "field" node of the AST should be passed in.
        :param ctxt: A clone of the context right before the templated struct was evaluated. It shouldn't have the
        templated struct in it.
        """
        self.params = params
        self.fields = fields
        self.ctxt = ctxt

    def resolve(self, args: list[lark.Tree], calc: Calculate) -> Struct:
        """
        Resolve the template, given a substitution specified by the given args.

        A wrinkle is that template syntax is somewhat ambiguous, so we can't tell if something is supposed to be a type
        or a constexpr until we know what the template is. So we just pass in the full AST nodes for the arguments
        and resolve them specially once we figure out whether each argument should be a constexpr or a type. This is why
        we pass in the Calculator instance, so we can do that "resolve them specially" part.

        :param args: The arguments of the template expansion. Should be either "type" or a "const_expr" AST nodes.
        :param calc: The Calculator instance in which the template expansion was needed.
        :return: A Struct representing the result of the template expansion.
        """
        if len(args) != len(self.params):
            raise Exception()
        resolve_ctxt = self.ctxt.clone()
        for arg, (param_type, param_name) in zip(args, self.params):
            if param_type == "typename":
                typ = calc.as_type(arg)
                resolve_ctxt.types[param_name] = typ
            else:
                val = calc.as_const_expr(arg)
                resolve_ctxt.names[param_name] = val
        calc = Calculate(resolve_ctxt)
        fields: dict[str, Type] = {}
        for item in self.fields:
            f_name, field = calc.visit(item)
            fields[f_name] = field
        return Struct(fields)


class Context:
    """
    A convenience class which binds together the three aspects tracked in a namespace (for our purposes), that being
    constants, types, and templates.
    """
    def __init__(self, names: dict[str, int], types: dict[str, Type], templates: dict[str, Template]):
        self.names = names
        self.types = types
        self.templates = templates

    def clone(self) -> Context:
        """
        Creates a copy of the context, so we can change one without affecting the other.
        """
        return Context(self.names.copy(), self.types.copy(), self.templates.copy())


class Calculate(Interpreter):
    """
    The primary workhorse class, it takes in AST nodes and a Context, and outputs into that Context the data types
    that were defined in the AST nodes.
    """
    def __init__(self, ctxt: Context):
        self.ctxt = ctxt
        self.names = ctxt.names
        self.types = ctxt.types
        self.templates = ctxt.templates

    def start(self, top_levels: lark.Tree):
        self.visit_children(top_levels)

    @v_args(inline=True)
    def enum(self, name: lark.Token, *variants: lark.Tree):
        enum = {}
        for i, variant in enumerate(variants):
            enum[i] = self.visit(variant)
        self.types[str(name)] = Enum(enum)

    @v_args(inline=True)
    def enum_variant(self, name: lark.Token):
        return str(name)

    @v_args(inline=True)
    def struct(self, name: lark.Token, items: lark.Tree):
        fields: dict[str, Type] = {}
        for item in items.children:
            if item.data == "field":
                f_name, field = self.visit(item)
                fields[f_name] = field
        self.types[str(name)] = Struct(fields)

    @v_args(inline=True)
    def template_param_type(self, name: lark.Token) -> tuple[str, str]:
        return "typename", str(name)

    @v_args(inline=True)
    def template_param_const(self, typ: lark.Tree, name: lark.Token) -> tuple[str, str]:
        return "const", str(name)

    @v_args(inline=True)
    def templated_struct(self, template: lark.Tree, name: lark.Token, items: lark.Tree):
        template_params = []
        for template_param in template.children:
            template_params.append(self.visit(template_param))

        fields: list[lark.Tree] = []
        for item in items.children:
            if item.data == "field":
                fields.append(item)
        self.templates[str(name)] = Template(template_params, fields, self.ctxt.clone())

    @v_args(inline=True)
    def field(self, decl: lark.Tree, init: lark.Tree = None) -> tuple[str, Type]:
        return self.visit(decl)

    @v_args(inline=True)
    def decl(self, typ: lark.Tree, name: lark.Token, *arrays: lark.Tree) -> tuple[str, Type]:
        base: Type = self.visit(typ)
        for array in arrays:
            count: int = self.visit(array)
            base = Array(base, count)
        return str(name), base

    def as_type(self, tree: lark.Tree) -> Type:
        if tree.data in ("ident", "type_name"):
            return self.type_name(tree)
        else:
            return self.type_generic(tree)

    def as_const_expr(self, tree: lark.Tree) -> int:
        if tree.data in ("ident", "type_name"):
            return self.ident(tree)
        else:
            return self.integer(*tree.children)

    @v_args(inline=True)
    def ident(self, name: lark.Token) -> int:
        return self.names[str(name)]

    @v_args(inline=True)
    def integer(self, num: lark.Token) -> int:
        if num.type == "DECIMAL":
            return int(num.value)
        elif num.type == "HEX":
            return int(num.value[2:], 16)
        elif num.type == "BINARY":
            return int(num.value[2:], 2)
        elif num.type == "OCT":
            return int(num.value[2:], 8)
        else:
            raise Exception()

    @v_args(inline=True)
    def type_name(self, name: lark.Token) -> Type:
        return self.types[str(name)]

    @v_args(inline=True)
    def type_generic(self, name: lark.Token, args: lark.Tree) -> Type:
        thing = self.templates[str(name)].resolve(args.children, self)
        return thing


# this stuff is global for easier editing, I guess
# look at main to see how it's used
BASE_NAMES: dict[str, int] = {}
BASE_TYPES: dict[str, Type] = {
    'bool': Boolean(),
    'float': Float(4),
    'uint32_t': Integer(4, signed=False),
    'systime_t': Integer(4)
}
BASE_TEMPLATES: dict[str, Template] = {}
BASE_CTXT = Context(BASE_NAMES, BASE_TYPES, BASE_TEMPLATES)


def render_bytes(n: int) -> str:
    """
    A helper function which makes a number of bytes prettier by appending units.

    For example, if given 22200 bytes, this will display it as 22.20 kb.

    :param n: A number of bytes.
    :return: The number of bytes, with units (up to Tb) and 4 significant digits.
    """
    endings = ["", " kb", " Mb", " Gb", " Tb"]
    end_idx = 0
    while n >= 1000 and end_idx < len(endings):
        n /= 1000
        end_idx += 1
    return f"{n:#.4g}{endings[end_idx]}"


def get_arguments():
    """
    A helper function which parses the arguments passed to the file.

    Most notably, if the "out" parameter isn't supplied, it defaults
    to the "raw" path with the suffix changed to ".json".

    :return: An object which has three fields, each of which contains a pathlib.Path: 'header', 'raw', and 'out'.
    """
    parser = ArgumentParser(prog="data_parser")
    parser.add_argument("header", type=pathlib.Path)
    parser.add_argument("raw", type=pathlib.Path)
    parser.add_argument("-o", "--out", type=pathlib.Path)
    args = parser.parse_args()

    if args.out is None:
        raw_path: pathlib.Path = args.raw
        args.out = raw_path.with_suffix(".json")
    return args


def main():
    args = get_arguments()

    parser = Lark(grammar, parser="earley")
    # open up the header file and read it in
    with args.header.open("r") as f:
        text = f.read()
    # parse the text into an AST made of lark.Tree and lark.Token
    tree = parser.parse(text)
    # create the global namespace, containing the default types like `bool` and `int`
    ctxt = BASE_CTXT.clone()
    # create the base Calculate instance for the global namespace, then run it for the AST given
    calc = Calculate(ctxt)
    calc.visit(tree)

    # extract the info for the sensorDataStruct_t from the context (since Calculate mutates it as it goes)
    sensor_data_struct: Type = ctxt.types["sensorDataStruct_t"]

    # open up the raw data file and read it in
    with args.raw.open("rb") as f_da:
        all_data: bytes = f_da.read()

    idx = 0  # a counter which keeps track of how far into the raw data we are
    # open up the output file, which we write to incrementally
    with args.out.open("w") as f_out:
        f_out.write("[")
        prev = False  # keeps track of whether this is the first line written, so we know whether to prepend a comma
        while idx < len(all_data):
            # read in a slice of data equal to the size of sensorDataStruct_t, then increment the counter by that much
            raw = all_data[idx:idx+sensor_data_struct.size]
            idx += sensor_data_struct.size
            # if there wasn't enough data to read, end the loop
            if len(raw) < sensor_data_struct.size:
                break

            # use the Type.parse method in order to convert the raw binary to json
            out = sensor_data_struct.parse(raw)
            if prev:
                f_out.write(",\n")
            else:
                f_out.write("\n")
                prev = True
            # write the json to the output file
            f_out.write(repr(out))
            # displays the progress
            print(f"\rParsed {render_bytes(idx)}/{render_bytes(len(all_data))} bytes", end="", flush=True)
        f_out.write("\n]")


if __name__ == '__main__':
    main()
