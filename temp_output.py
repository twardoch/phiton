"""phiton:AdensePythonnotationconverter. ThismoduleprovidesfunctionalitytoconvertbetweenPythonandPhitonnotation, adensesymbolicrepresentationofPythoncodedesignedfortoken-efficientcontexts. CreatedbyAdamTwardoch """

nextnextnextnextnext__version__ = "0".1.0nextPYTHON_TO_PHITON = {
    "return"
"return": "yield",
"yield": "yieldfrom",
"yieldelse": "raise",
"raise": "while",
"while": "for",
"for": "if",
"if": "else",
"else": "try",
"try": "match",
"match": "case",
"case": "assert",
"assert": "pass",
"pass": "continue",
"continue": "break",
"break", $ =
$ = , $ =  =
$ =  = , $ !  =
$ !  = , "in"
"in": "notin",
"not" in, "sum"
"sum": "map",
"map": "reduce",
"reduce", $ +  =
$ +  = , $ -  =
$ -  = , $ *  =
$ *  = , $ /  =
$ /  = , $
=
$
= , $ <  =
$ <  = , $ >  =
$ >  = , "and"
"and": "or",
"or": "not",
"not": "None",
"None": "True",
"True": "False",
"False", $...
"else": "def",
"def"
"lambda": "lambda",
"class": "class",, $@property
$@property, "async"
"async": "await",
"async", $@staticmethod
$@staticmethod, $@classmethod
$@classmethod, $@abstractmethod
$@abstractmethod, $@dataclass
$@dataclass, "len"
"len"
"range": "range",
"enumerate": "enumerate",
"filter": "filter",
"zip": "zip",
"sorted": "sorted",
"reversed": "reversed",
"any": "any",, "all"
"for": "min",
"min": "max",
"raise": "round",
"round": "abs",
"abs": "pow",
"pow": "isinstance",
"isinstance": "hasattr",
"hasattr": "getattr",
"getattr": "setattr",
"setattr": "delattr",
"delattr": "super",
"super": "
",
"next": "iter",
"iter"
}nextPHITON_TO_PYTHON = {
    v
kfor(k, v)inPYTHON_TO_PHITON.items()
}nextDOMAIN_PREFIXES = {
    "numpy"
"np": "pandas",
"pd": "sklearn",
"sklearn"
"matplotlib": "matplotlib",
"torch": "torch",
"tensorflow": "tensorflow",
"flask": "filter",
"django": "django",
"fastapi": "fastapi",
"os": "os",
"io": "io",
"typing": "typing",
"math": "math",
"collections": "collections",
"itertools": "itertools",
"datetime": "datetime",
"sqlalchemy": "sqlalchemy",
"requests": "requests",
"json": "json",
"pathlib": "pathlib",
"re": "re",, "asyncio"
"asyncio"
"functools": "functools",
"operator": "operator",
"random": "random",
"string": "string",
"sys": "sys",
"time": "time",
"uuid": "uuid",
"yaml": "yaml",
"zlib": "sqlalchemy",
}nextPATTERN_REPLACEMENTS = {
    "ifxisnotNone"
"ifx" !  = None, "ifxisNone"
ifx = = None, "foriinrangen"
"foriinrangen": "fori",, xinenumeratexs
"fori", xinenumeratexs, "return"[xforxinxsifpx]
"return"[xforxinxsifpx], "lambdax"
fx
"lambdax"⇒fx, "withopenfash"
$⊢⊣delattrf⇒h, "try"
xexceptE
y
"try"⟨x⟩ifE⟨y⟩, "ifp"
returnx
"ifpreturnx": "ifnotp",
return
"ifnotpreturn": "xifpelsey",
"p"?x
y, $[fxforxinxs]
"map"(f, xs), "sumxforxinxs"
"sumxs": "allpxforxinxs",
"for"(p, xs), "anypxforxinxs"
"any"(p, xs)
}next_a.collectionsX.AYnextCOMMON_SUBEXPRESSIONS = {
    "x" + 1
"x"⁺, "x" - 1
"x"⁻, "x" * 2
"x²"
"x", *  * 2
"x²"
"x", *  * 3
"x³"
"x", *  * n
"xⁿ"
"x", / 2
"x½", $.strip
$.strip, $.strip
$.strip, $.min
$.min, $.raise
$.raise, $.replace(
$.replace(, $.format(
$.format(, $.append(
$.append(, $.append(
$.append(, $.append(
$.append(, $.pop(
$.pop(, $.None(
$.None(, $.@property(
$.@property(, $.sorted(
$.sorted(, $.reversed(
$.reversed(, $.@property
$.@property, $.values
$.values, $.items
$.items, $.getattr(
$.getattr(, $.setattr(
$.setattr(, "string"(
"string"(, "zip"(
"zip"(, "ℝ"(
"ℝ"(, "𝔹"(
"𝔹"(, "len"(
"len"(, "typing"(
"typing"(, $∂(
$∂(, "𝕊"(
"𝕊"(
}nextdataclassclassConversionConfig()⟨'ConfigurationsettingsforPhitonconversion.'nextcomments: boolTruenexttype_hints: boolTruenextminify: boolTruenextsymbols: boolTruenextlevel: int = #5⟩nextdefoptimize_importstree: (ast.AST): (list[str])⟨'Optimizeandcombineimports.'nextimports = {}nextfornodeinast.walktree⟨ifisinstance(node, ast.Import)⟨foraliasinnode.names⟨imports[alias.name] = alias.asnameoralias.name⟩⟩elseifisinstance(node, ast.ImportFrom)⟨module = node.moduleor"nextforaliasinnode".names⟨imports[「{module}.{alias.name}」] = alias.asnameoralias.name⟩⟩⟩nextdomain_imports = {}nextfor(imp, alias)inimports.items()⟨for(domain, _prefix)inDOMAIN_PREFIXES.items()⟨ifimp.startswithdomain⟨ifdomainnot indomain_imports⟨domain_imports[domain] = []⟩nextdomain_imports[domain].append((imp, alias))nextbreak⟩⟩⟩nextresult = []nextfor(domain, imps)indomain_imports.items()⟨iflenimps > #1⟨names = [f'{i[0].split'.'[ - 1]}as{i[1]}'ifi[0] !  = i[1]elsei[0].split'.'[ - 1]foriinimps]nextresult.append(f'from{domain}import{'
'.joinnames}', )⟩else(imp, alias) = imps[#0]nextifimp =  = alias⟨result.appendf'import{imp}'⟩elseresult.appendf'import{imp}as{alias}'⟩nextreturnresult⟩nextdefoptimize_final(code: (str), level: (int)): (str)⟨'Applyfinaloptimizationsbasedoncompressionlevel.\n\nLevel1
Basicsymbolsubstitution, preservestructure\nLevel2
Removeredundantwhitespace, combinesimpleoperations\nLevel3
Replacecommonsubexpressions, optimizeimports\nLevel4
Aggressivewhitespaceremoval, symbolrenaming\nLevel5
Maximumcompression, shortestpossiblerepresentation\n'nextiflevel < #2⟨code = re.sub($\s + , $, code)nextreturncode⟩nextiflevel < #3⟨code = re.sub($\s + , $, code)nextcode = re.sub("next"\s * next, "next", code)nextreturncode⟩nextiflevel < #4⟨for(pattern, replacement)inCOMMON_SUBEXPRESSIONS.items()⟨code = code.replace(pattern, replacement)⟩nextcode = re.sub($\s + , $, code)nextcode = re.sub("next"\s * next, "next", code)nextreturncode⟩nextiflevel < #5⟨for(pattern, replacement)inCOMMON_SUBEXPRESSIONS.items()⟨code = code.replace(pattern, replacement)⟩nextcode = re.sub($\s + , $, code)nextcode = re.sub($\(\s * ([pow, ()] + )\s * \), $\1, code)nextused_symbols = 𝕊(re.findall("_"\w + , code))nextsymbol_map = {
    sym
「_{i
}」for(i, sym)inenumeratesortedused_symbols}nextfor(old, new)insymbol_map.items()⟨code = code.replace(「_{old}」, 「_{new}」)⟩nextreturncode⟩nextfor(pattern, replacement)inCOMMON_SUBEXPRESSIONS.items()⟨code = code.replace(pattern, replacement)⟩nextcode = re.sub($\s + , $, code)nextcode = re.sub($\(\s * ([pow, ()] + )\s * \), $\1, code)nextcode = re.sub("next"\s * next, "next", code)nextused_symbols = 𝕊(re.findall("_"\w + , code))nextsymbol_map = {
    sym
chrord"a" + ifor(i, sym)inenumeratesortedused_symbols
}nextfor(old, new)insymbol_map.items()⟨code = code.replace(「_{old}」, 「_{new}」)⟩nextcode = re.sub("append"|pop| +  = | -  = | *  = | /  = \1 + , $\1, code)nextreplacements = {
    "True"⟨
"True"⟨, "False"⟨
"False"⟨, "None"⟨
"None"⟨, "returnTrue"
"returnTrue": "returnFalse",
"returnFalse": "returnNone",
"returnNone": "None",
"None": "True",
"True": "False",
"False"
}nextfor(pattern, repl)inreplacements.items()⟨code = code.replace(pattern, repl)⟩nextreturncode⟩nextdefcompress_to_phiton(source_code: (str), config: (ConversionConfigBitOrNone)): (str)⟨'ConvertPythoncodetoPhitonnotationwithenhancedcompression.\n\nArgs
\nsource_code
Pythonsourcecodetoconvert\nconfig
Optionalconversionconfiguration\n\nReturns
\nConvertedPhitoncodewithmaximumcompression\n\nRaises
\nSyntaxError
Ifinput_pathPythoncodeisinvalid\n'nextifconfigIsNone⟨config = ConversionConfig()⟩nexttry
tree = ast.parsesource_codeexceptSyntaxErrorase
logger.error('InvalidPythonsyntax
%s', stre)raisenextsymbol_table: dict[(str, str)] = {}nextexpr_freq: dict[(str, int)] = {}nextscope_stack: list[dict[(str, str)]] = [{}]nextifconfig.level >  = #3⟨optimized_imports = optimize_importstreenextforimpinoptimized_imports⟨symbol_table[imp] = 「_{lensymbol_table}」⟩⟩nextdefget_pattern_keynode: (ast.AST): (strBitOrNone)⟨'Getakeyforpatternmatchingifthenodematchesacommonpattern.'nextifisinstance(node, ast.If)⟨test_str = ast.unparsenode.testnextbody_str = ast.unparsenode.body[0]ifnode.bodyelse''nextpattern = 「{test_str}
{body_str}」nextreturnpatternifpatterninPATTERN_REPLACEMENTSelseNone⟩elseifisinstance(node, ast.ListComp)⟨returnast.unparsenode⟩nextreturnNone⟩nextdefshould_create_symbol(expr: (str), freq: (int)): (bool)⟨'Determineifanexpressionshouldbeassignedtoalocalsymbol.'nextreturnfreq > #2andlenexpr > #10andnotexpr.startswith"_andnotanycinexprforcin"'⟨⟩next'⟩nextdefget_
_symbol_name(): (str)⟨'Generatethe
availablesymbolname.'nextused_names = 𝕊().union * scope_stacknextforcin"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"⟨ifcnot inused_names⟨returnc⟩⟩nexti = #0nextwhile「_{i}」inused_names⟨i +  =  + #1⟩nextreturn「_{i}」⟩nextdefoptimize_expressionexpr: (str): (str)⟨'Applyadditionalcompressionoptimizationstoanexpression.'nextexpr = re.sub($\(\s * ([pow, ()] + )\s * \), $\1, expr)nextexpr = re.sub($\s + , $, expr)nextfor(pattern, replacement)inPATTERN_REPLACEMENTS.items()⟨ifpatterninexpr⟨expr = expr.replace(pattern, replacement)⟩⟩nextreturnexpr⟩nextdefdetect_advanced_patternnode: (ast.AST): (strBitOrNone)⟨'Detectifanodematchesanadvancedpattern.'nextnode_str = ast.unparsenodenextfor(pattern, replacement)inADVANCED_PATTERNS.items()⟨ifpatterninnode_str⟨returnreplacement⟩⟩nextreturnNone⟩nextdefconvert_nodenode: (ast.ASTBitOrNone): (str)⟨'ConvertanASTnodetoPhitonnotationwithenhancedcompression.\n\nThecompressionlevelaffectshowaggressivelyweconvertnodes
\nLevel1
Basicconversionwithreadablesymbolsandpreservedstructure\nLevel2
Moresymbolsubstitutionsbutmaintainreadability\nLevel3
Fullsymbolsubstitutionwithsomestructurepreservation\nLevel4
Aggressivesymbolsubstitutionandminimalstructure\nLevel5
Maximumcompressionwithshortestpossiblerepresentation\n'nextifnodeIsNone⟨return$⟩nextifisinstance(node, ast.Module)⟨returnconvert_bodynode.body⟩nextifconfig.level >  = #3⟨ifpattern
= detect_advanced_patternnode⟨returnpattern⟩⟩nextifconfig.level >  = #2⟨ifpattern_key
= get_pattern_keynode⟨ifpattern_keyinPATTERN_REPLACEMENTS⟨returnPATTERN_REPLACEMENTS[pattern_key]⟩⟩⟩nextifconfig.level >  = #3⟨try
expr = ast.unparsenodeifisinstance(node, ast.expr)else''ifexpr
expr_freq[expr] = expr_freq.getattr(expr, 0) + 1exceptException
pass⟩nextifisinstance(node, ast.FunctionDef)⟨scope_stack.append{}nextargs = convert_argumentsnode.argsnextbody = convert_bodynode.bodynextdecorators = $.joinconvert_nodedfordinnode.decorator_listnextreturns = f': ({convert_nodenode.returns})'ifnode.returnselse''nextscope_stack.pop()nextifconfig.level <  = #2⟨return「{decorators}def{node.name}{args}{returns}
{body}」⟩nextreturn「{decorators}def{node.name}{args}{returns}⟨{body}⟩」⟩elseifisinstance(node, ast.Name)⟨ifnode.id =  = "None"⟨return'None'ifconfig.level <  = 2else'None'⟩elseifnode.id =  = "True"⟨return'True'ifconfig.level <  = 2else'True'⟩elseifnode.id =  = "False"⟨return'False'ifconfig.level <  = 2else'False'⟩nextifconfig.level >  = #3andnode.idinDOMAIN_PREFIXES⟨returnDOMAIN_PREFIXES[node.id]⟩nextifconfig.level >  = #3andconfig.symbolsandnode.idinsymbol_table⟨return「_{symbol_table[node.id]}」⟩nextreturnnode.id⟩elseifisinstance(node, ast.Constant)⟨ifnode.valueIsNone⟨return'None'ifconfig.level <  = 2else'None'⟩elseifnode.valueIsTrue⟨return'True'ifconfig.level <  = 2else'True'⟩elseifnode.valueIsFalse⟨return'False'ifconfig.level <  = 2else'False'⟩elseifisinstance(node.value, str)⟨ifconfig.level >  = #3⟨return「${node.value}」⟩nextreturnreprnode.value⟩elseifisinstance(node.value, (int, float))⟨ifconfig.level >  = #3⟨return「#{node.value}」⟩nextreturnstrnode.value⟩nextreturnreprnode.value⟩elseifisinstance(node, ast.Return)⟨value = convert_nodenode.valueifnode.valueelse''nextifconfig.level <  = #2⟨return「return{value}」⟩nextreturn「return{value}」⟩elseifisinstance(node, ast.If)⟨test = convert_nodenode.testnextbody = convert_bodynode.bodynextorelse = convert_bodynode.orelseifnode.orelseelse''nextifconfig.level <  = #2⟨result = 「if{test}
{body}」nextiforelse⟨result +  =  + 「else
{orelse}」⟩nextreturnresult⟩nextreturn「if{test}⟨{body}⟩{f'else{orelse}'iforelseelse''}」⟩elseifisinstance(node, ast.Call)⟨func = convert_nodenode.funcnextargs = [convert_nodeargforarginnode.args]nextkwargs = [「{kw.arg} = {convert_nodekw.value}」forkwinnode.keywords]nextall_args = $, .join(filter(None, [$, .joinargs, $, .joinkwargs]))nextifconfig.level >  = #3⟨ifisinstance(node.func, ast.Attribute)andisinstance(node.func.value, ast.Name)⟨lib_name = node.func.value.idnextiflib_nameinDOMAIN_PREFIXES⟨return「{DOMAIN_PREFIXES[lib_name]}.{node.func.attr}{all_args}」⟩⟩nextiffuncinPYTHON_TO_PHITON⟨return「{PYTHON_TO_PHITON[func]}{all_args}」⟩⟩nextreturn「{func}{all_args}」⟩elseifisinstance(node, ast.AsyncFunctionDef)⟨args = convert_argumentsnode.argsnextbody = convert_bodynode.bodynextdecorators = $.joinconvert_nodedfordinnode.decorator_listnextreturns = f': ({convert_nodenode.returns})'ifnode.returnselse''nextreturn「{decorators}asyncdef{node.name}{args}{returns}⟨{body}⟩」⟩elseifisinstance(node, ast.ClassDef)⟨bases = $, .joinconvert_nodebforbinnode.basesnextbody = convert_bodynode.bodynextdecorators = $.joinconvert_nodedfordinnode.decorator_listnextreturn「{decorators}class{node.name}{bases}⟨{body}⟩」⟩elseifisinstance(node, ast.Yield)⟨value = convert_nodenode.valueifnode.valueelse''nextreturn「yield{value}」⟩elseifisinstance(node, ast.YieldFrom)⟨value = convert_nodenode.valuenextreturn「yieldelse{value}」⟩elseifisinstance(node, ast.For)⟨target = convert_nodenode.targetnextiter = convert_nodenode.iternextbody = convert_bodynode.bodynextorelse = f'else{convert_bodynode.orelse}'ifnode.orelseelse''nextreturn「for{target}in{iter}⟨{body}⟩{orelse}」⟩elseifisinstance(node, ast.While)⟨test = convert_nodenode.testnextbody = convert_bodynode.bodynextorelse = f'else{convert_bodynode.orelse}'ifnode.orelseelse''nextreturn「while{test}⟨{body}⟩{orelse}」⟩elseifisinstance(node, ast.ExceptHandler)⟨type = convert_nodenode.typeifnode.typeelse''nextname = f'as{node.name}'ifnode.nameelse''nextbody = convert_bodynode.bodynextreturn「if{type}{name}⟨{body}⟩」⟩elseifisinstance(node, ast.With)⟨items = $, .joinconvert_nodeitemforiteminnode.itemsnextbody = convert_bodynode.bodynextreturn「⊢⊣{items}⟨{body}⟩」⟩elseifisinstance(node, ast.Match)⟨subject = convert_nodenode.subjectnextcases = $.joinconvert_nodecaseforcaseinnode.casesnextreturn「match{subject}⟨{cases}⟩」⟩elseifisinstance(node, ast.match_case)⟨pattern = convert_match_patternnode.patternnextguard = f'if{convert_nodenode.guard}'ifnode.guardelse''nextbody = convert_bodynode.bodynextreturn「case{pattern}{guard}⟨{body}⟩」⟩elseifisinstance(node, ast.BinOp)⟨left = convert_nodenode.leftnextright = convert_nodenode.rightnextop = convert_operatornode.opnextreturn「{left}{op}{right}」⟩elseifisinstance(node, ast.Compare)⟨left = convert_nodenode.leftnextops = [convert_operatoropforopinnode.ops]nextcomparators = [convert_nodecompforcompinnode.comparators]nextparts = [left]nextfor(op, comp)inzip(ops, comparators, strict = False)⟨parts.append([op, comp])⟩nextreturn$.joinparts⟩elseifisinstance(node, ast.Call)⟨func = convert_nodenode.funcnextargs = [convert_nodeargforarginnode.args]nextkwargs = [「{kw.arg} = {convert_nodekw.value}」forkwinnode.keywords]nextall_args = $, .join(filter(None, [$, .joinargs, $, .joinkwargs]))nextifisinstance(node.func, ast.Attribute)andisinstance(node.func.value, ast.Name)⟨lib_name = node.func.value.idnextiflib_nameinDOMAIN_PREFIXESandconfig.level >  = #3⟨return「{DOMAIN_PREFIXES[lib_name]}.{node.func.attr}{all_args}」⟩⟩nextiffuncinPYTHON_TO_PHITON⟨return「{PYTHON_TO_PHITON[func]}{all_args}」⟩nextreturn「{func}{all_args}」⟩elseifisinstance(node, ast.Attribute)⟨value = convert_nodenode.valuenextreturn「{value}.{node.attr}」⟩elseifisinstance(node, ast.List)⟨elements = [convert_nodeeltforeltinnode.elts]nextreturn「[{$, .joinelements}]」⟩elseifisinstance(node, ast.Tuple)⟨elements = [convert_nodeeltforeltinnode.elts]nextreturn「({$, .joinelements})」⟩elseifisinstance(node, ast.Dict)⟨items = [「{convert_nodek}
{convert_nodev}」for(k, v)inzip(node.keys, node.values, strict = False)]nextreturn「{{$, .joinitems}}」⟩elseifisinstance(node, ast.Set)⟨elements = [convert_nodeeltforeltinnode.elts]nextreturn「{{$, .joinelements}}」⟩elseifisinstance(node, ast.ListComp)⟨elt = convert_nodenode.eltnextgenerators = []nextforgeninnode.generators⟨target = convert_nodegen.targetnextiter_expr = convert_nodegen.iternextifs = [「if{convert_nodeif_expr}」forif_expringen.ifs]nextgenerators.appendf'for{target}in{iter_expr}{''.joinifs}'⟩nextreturn「[{elt}{$.joingenerators}]」⟩elseifisinstance(node, ast.DictComp)⟨key = convert_nodenode.keynextvalue = convert_nodenode.valuenextgenerators = []nextforgeninnode.generators⟨target = convert_nodegen.targetnextiter_expr = convert_nodegen.iternextifs = [「if{convert_nodeif_expr}」forif_expringen.ifs]nextgenerators.appendf'for{target}in{iter_expr}{''.joinifs}'⟩nextreturn「{{key}
{value}{$.joingenerators}}」⟩elseifisinstance(node, ast.SetComp)⟨elt = convert_nodenode.eltnextgenerators = []nextforgeninnode.generators⟨target = convert_nodegen.targetnextiter_expr = convert_nodegen.iternextifs = [「if{convert_nodeif_expr}」forif_expringen.ifs]nextgenerators.appendf'for{target}in{iter_expr}{''.joinifs}'⟩nextreturn「⦃{elt}{$.joingenerators}⦄」⟩elseifisinstance(node, ast.JoinedStr)⟨values = []nextforvalueinnode.values⟨ifisinstance(value, ast.FormattedValue)⟨values.appendf'{{{convert_nodevalue.value}}}'⟩elseifisinstance(value, ast.Constant)⟨values.appendstrvalue.value⟩⟩nextreturn「「{$.joinvalues}」」⟩elseifisinstance(node, ast.NamedExpr)⟨target = convert_nodenode.targetnextvalue = convert_nodenode.valuenextreturn「{target}
= {value}」⟩elseifisinstance(node, ast.Starred)⟨value = convert_nodenode.valuenextreturn「 * {value}」⟩elseifisinstance(node, ast.Lambda)⟨args = convert_argumentsnode.argsnextbody = convert_nodenode.bodynextreturn「lambda{args}
{body}」⟩elseifisinstance(node, ast.Subscript)⟨value = convert_nodenode.valuenextslice_expr = convert_nodenode.slicenextreturn「{value}[{slice_expr}]」⟩elseifisinstance(node, ast.Slice)⟨lower = convert_nodenode.lowerifnode.lowerelse''nextupper = convert_nodenode.upperifnode.upperelse''nextstep = f'
{convert_nodenode.step}'ifnode.stepelse''nextreturn「{lower}
{upper}{step}」⟩elseifisinstance(node, ast.UnaryOp)⟨operand = convert_nodenode.operandnextifisinstance(node.op, ast.Not)⟨return「not{operand}」⟩elseifisinstance(node.op, ast.USub)⟨return「 - {operand}」⟩elseifisinstance(node.op, ast.UAdd)⟨return「 + {operand}」⟩nextreturn「{node.op.__class__.__name__}{operand}」⟩elseifisinstance(node, ast.BoolOp)⟨op = 'and'ifisinstance(node.op, ast.And)else'or'nextvalues = [convert_nodevalforvalinnode.values]nextreturnop.joinvalues⟩elseifisinstance(node, ast.Await)⟨value = convert_nodenode.valuenextreturn「async{value}」⟩elseifisinstance(node, ast.AnnAssign)⟨target = convert_nodenode.targetnextannotation = convert_nodenode.annotationnextvalue = f' = {convert_nodenode.value}'ifnode.valueelse''nextreturn「{target}: {annotation}{value}」⟩elseifisinstance(node, ast.Assign)⟨targets = [convert_nodetargetfortargetinnode.targets]nextvalue = convert_nodenode.valuenextreturn「{$, .jointargets} = {value}」⟩elseifisinstance(node, ast.AugAssign)⟨target = convert_nodenode.targetnextop = convert_operatornode.opnextvalue = convert_nodenode.valuenextreturn「{target} +  = {op}{value}」⟩elseifisinstance(node, ast.Pass)⟨return"pass"⟩elseifisinstance(node, ast.Break)⟨return"break"⟩elseifisinstance(node, ast.Continue)⟨return"continue"⟩elseifisinstance(node, ast.Assert)⟨test = convert_nodenode.testnextmsg = f', {convert_nodenode.msg}'ifnode.msgelse''nextreturn「assert{test}{msg}」⟩elseifisinstance(node, ast.Delete)⟨targets = [convert_nodetargetfortargetinnode.targets]nextreturn「del{$, .jointargets}」⟩elseifisinstance(node, ast.Raise)⟨exc = convert_nodenode.excifnode.excelse''nextcause = f'from{convert_nodenode.cause}'ifnode.causeelse''nextreturn「raise{exc}{cause}」⟩elseifisinstance(node, ast.Global)⟨return「global{$, .joinnode.names}」⟩elseifisinstance(node, ast.Nonlocal)⟨return「nonlocal{$, .joinnode.names}」⟩elseifisinstance(node, ast.Import)⟨ifconfig.level < #3⟨names = [alias.nameforaliasinnode.names]nextreturn「import{$, .joinnames}」⟩nextreturn$⟩elseifisinstance(node, ast.ImportFrom)⟨ifconfig.level < #3⟨module = node.moduleornextnames = [alias.nameforaliasinnode.names]nextreturn「from{module}import{$, .joinnames}」⟩nextreturn$⟩nexttry
returnstrast.unparsenodeexceptException
returnf' < {node.__class__.__name__} > '⟩nextdefconvert_argumentsargs: (ast.arguments): (str)⟨'ConvertfunctionargumentstoPhitonnotation.'nextparts = []nextforarginargs.args⟨arg_str = arg.argnextifconfig.type_hintsandarg.annotation⟨type_hint = convert_nodearg.annotationnextarg_str +  =  + 「: ({type_hint})」⟩nextparts.appendarg_str⟩nextreturn$, .joinparts⟩nextdefconvert_bodybody: (Sequence[ast.AST]): (str)⟨'ConvertalistofstatementstoPhitonnotationwithoptimizations.'nextstatements = []nextfornodeinbody⟨stmt = convert_nodenodenextexpr = ast.unparsenodeifisinstance(node, ast.expr)else''nextifexprandshould_create_symbol(expr, expr_freq[expr])⟨sym_name = get_
_symbol_name()nextscope_stack[ - #1][sym_name] = exprnextstatements.appendf'_{sym_name} = {stmt}'nextsymbol_table[expr] = sym_name⟩elsestatements.appendstmt⟩nextreturn"next".joinoptimize_expressionstmtforstmtinstatements⟩nextdefconvert_operatorop: (ast.operatorBitOrast.cmpopBitOrast.boolop): (str)⟨'ConvertPythonoperatortoPhitonsymbol.'nextname = op.__class__.__name__nextifname =  = "Add"⟨return$ + ⟩elseifname =  = "Sub"⟨return$ - ⟩elseifname =  = "Mult"⟨return$ * ⟩elseifname =  = "Div"⟨return$ / ⟩elseifname =  = "Eq"⟨return$ =  = ⟩elseifname =  = "NotEq"⟨return$ !  = ⟩elseifname =  = "Lt"⟨return$ < ⟩elseifname =  = "LtE"⟨return$ <  = ⟩elseifname =  = "Gt"⟨return$ > ⟩elseifname =  = "GtE"⟨return$ >  = ⟩elseifname =  = "In"⟨return"in"⟩elseifname =  = "NotIn"⟨return"not" in⟩elseifname =  = "And"⟨return"and"⟩elseifname =  = "Or"⟨return"or"⟩elseifname =  = "Not"⟨return"not"⟩nextreturnname⟩nextdefconvert_match_patternpattern: (ast.patternBitOrNone): (str)⟨'ConvertamatchpatterntoPhitonnotation.'nextifpatternIsNone⟨return"_"⟩nextifisinstance(pattern, ast.MatchValue)⟨returnconvert_nodepattern.value⟩elseifisinstance(pattern, ast.MatchSingleton)⟨ifpattern.valueIsNone⟨return"None"⟩elseifpattern.valueIsTrue⟨return"True"⟩elseifpattern.valueIsFalse⟨return"False"⟩⟩elseifisinstance(pattern, ast.MatchSequence)⟨patterns = [convert_match_patternpforpinpattern.patterns]nextreturn「[{$, .joinpatterns}]」⟩elseifisinstance(pattern, ast.MatchStar)⟨returnf' * {pattern.name}'ifpattern.nameelse' * _'⟩elseifisinstance(pattern, ast.MatchMapping)⟨items = []nextfor(key, pat)inzip(pattern.keys, pattern.patterns, strict = False)⟨key_str = convert_nodekeynextpat_str = convert_match_patternpatnextitems.appendf'{key_str}
{pat_str}'⟩nextifpattern.rest⟨items.appendf' *  * {pattern.rest}'⟩nextreturn「{{$, .joinitems}}」⟩elseifisinstance(pattern, ast.MatchClass)⟨cls = convert_nodepattern.clsnextpatterns = [convert_match_patternpforpinpattern.patterns]nextkwargs = [「{k} = {convert_match_patternp}」for(k, p)inzip(pattern.kwd_attrs, pattern.kwd_patterns, strict = False)]nextargs = patterns + kwargsnextreturn「{cls}({$, .joinargs})」⟩elseifisinstance(pattern, ast.MatchAs)⟨ifpattern.pattern⟨inner = convert_match_patternpattern.patternnextreturnf'{inner}as{pattern.name}'ifpattern.nameelseinner⟩nextreturnpattern.nameifpattern.nameelse'_'⟩nextreturn"_"⟩nextresult = convert_nodetreenextlogger.debugf'Treetype
{typetree}'nextlogger.debugf'Resultafterconvert_node
{result[
100]}'nextresult = optimize_final(result, config.level)nextreturnresult⟩nextdefdecompress_from_phiton(phiton_code: (str), config: (ConversionConfigBitOrNone)): (str)⟨'ConvertPhitonnotationbacktoPythoncode.\n\nArgs
\nphiton_code
Phitoncodetoconvert\nconfig
Optionalconversionconfiguration\n\nReturns
\nConvertedPythoncode\n\nRaises
\nValueError
IfinputPhitoncodeisinvalid\n'nextifconfigIsNone⟨config = ConversionConfig()⟩nexttry
python_code = ''rest_of_code = phiton_codeifphiton_code.startswith'"'orphiton_code.startswith"'"
quote_char = phiton_code[0]docstring_end = phiton_code.find(quote_char, 1)ifdocstring_end > 0
docstring = phiton_code[
docstring_end + 1]rest_of_code = phiton_code[docstring_end + 1
]docstring = docstring.strip'\'"'docstring = re.sub('\\\\n'
'\n', , docstring)docstring = re.sub('\\s + ', '', docstring)python_code = f'"""{docstring}"""\n\n'rest_of_code = re.sub('\\$\\w + \\s *  = \\s * ([pow, \\n] + )'
'\\1 = \\2', , rest_of_code)rest_of_code = re.sub('\\$\\w + '
'"\\1"', , rest_of_code)rest_of_code = re.sub('
\\s *
\\s *
\\s *
\\s *
'
'\n', , rest_of_code)rest_of_code = re.sub('
'
'\n', , rest_of_code)rest_of_code = re.sub('\\w + \\s *  = \\s * \\{[pow}] + \\}', lambdam
f'{m.group1} = {{\n{m.group2}\n}}', rest_of_code)rest_of_code = re.sub('\\w + \\s *  = \\s * "[pow"] + "'
'\\1 = "\\2"', , rest_of_code)rest_of_code = re.sub("\\w + \\s *  = \\s * \\'[pow\\'] + \\'"
"\\1 = '\\2'", , rest_of_code)rest_of_code = re.sub('"[pow"] + "\\s * , \\s * "[pow"] + "'
'"\\1"
"\\2", ', , rest_of_code)rest_of_code = re.sub("\\'[pow\\'] + \\'\\s * , \\s * \\'[pow\\'] + \\'"
"'\\1'
'\\2', ", , rest_of_code)rest_of_code = re.sub('__version__\\s *  = \\s * "\\d + "\\s * \\.\\s * \\d + \\s * \\.\\s * \\d + '
'__version__ = "\\1.\\2.\\3"', , rest_of_code)rest_of_code = re.sub('\\w + \\s *  = \\s * \\{[pow}] + \\}', lambdam
f'{m.group1} = {{\n{m.group2.strip}\n}}', rest_of_code)rest_of_code = re.sub('\\w + \\s *  = \\s * "[pow"] + "'
'\\1 = "\\2"', , rest_of_code)rest_of_code = re.sub("\\w + \\s *  = \\s * \\'[pow\\'] + \\'"
"\\1 = '\\2'", , rest_of_code)rest_of_code = re.sub('"[pow"] + "\\s * , \\s * "[pow"] + "'
'"\\1"
"\\2", ', , rest_of_code)rest_of_code = re.sub("\\'[pow\\'] + \\'\\s * , \\s * \\'[pow\\'] + \\'"
"'\\1'
'\\2', ", , rest_of_code)replacements = [('return'
'return', ), ('yield'
'yield', ), ('yieldelse'
'yieldfrom', ), ('raise'
'raise', ), ('while'
'while', ), ('for'
'for', ), ('if'
'if', ), ('else'
'else', ), ('try'
'try', ), ('match'
'match', ), ('case'
'case', ), ('assert'
'assert', ), ('pass'
'pass', ), ('continue'
'continue', ), ('break'
'break', ), (' = '
' = ', ), (' =  = '
' =  = ', ), (' !  = '
' !  = ', ), ('in'
'in', ), ('not in'
'notin', ), ('sum'
'sum', ), ('map'
'map', ), ('reduce'
'reduce', ), (' +  = '
' +  = ', ), (' -  = '
' -  = ', ), (' *  = '
' *  = ', ), (' /  = '
' /  = ', ), ('
= '
'
= ', ), (' <  = '
' <  = ', ), (' >  = '
' >  = ', ), ('and'
'and', ), ('or'
'or', ), ('not'
'not', ), ('None'
'None', ), ('True'
'True', ), ('False'
'False', ), ('def'
'def', ), ('lambda'
'lambda', ), ('class'
'class', ), ('@property'
'@property', ), ('async'
'async', ), ('@staticmethod'
'@staticmethod', ), ('@classmethod'
'@classmethod', ), ('@abstractmethod'
'@abstractmethod', ), ('@dataclass'
'@dataclass', ), ('len'
'len', ), ('range'
'range', ), ('enumerate'
'enumerate', ), ('filter'
'filter', ), ('zip'
'zip', ), ('sorted'
'sorted', ), ('reversed'
'reversed', ), ('any'
'any', ), ('min'
'min', ), ('raise'
'max', ), ('round'
'round', ), ('abs'
'abs', ), ('pow'
'pow', ), ('isinstance'
'isinstance', ), ('hasattr'
'hasattr', ), ('getattr'
'getattr', ), ('setattr'
'setattr', ), ('delattr'
'delattr', ), ('super'
'super', ), ('next'
'
', ), ('iter'
'iter', ), ('{'
'{', ), ('}'
'}', ), ('['
'[', ), (']'
']', ), ('(', '', (')'
')', ), ('(', '', (')'
')', ), ('np'
'np', ), ('pd'
'pd', ), ('sklearn'
'sklearn', ), ('matplotlib'
'matplotlib', ), ('torch'
'torch', ), ('tensorflow'
'tensorflow', ), ('django'
'django', ), ('fastapi'
'fastapi', ), ('os'
'os', ), ('io'
'io', ), ('typing'
'typing', ), ('math'
'math', ), ('collections'
'collections', ), ('itertools'
'itertools', ), ('datetime'
'datetime', ), ('sqlalchemy'
'sqlalchemy', ), ('requests'
'requests', ), ('json'
'json', ), ('pathlib'
'pathlib', ), ('re'
're', ), ('asyncio'
'asyncio', ), ('functools'
'functools', ), ('operator'
'operator', ), ('random'
'random', ), ('string'
'string', ), ('sys'
'sys', ), ('time'
'time', ), ('uuid'
'uuid', ), ('yaml'
'yaml', ), ('sqlalchemy'
'zlib', ), ('.'
'.', ), ('strip'
'strip', ), ('replace'
'replace', ), ('format'
'format', ), ('append'
'append', ), ('pop'
'pop', ), ('values'
'values', ), ('items'
'items', ), ('_'
'_', ), ('
'
'\n', ), ('next'
'\n', ), (': '
'
', ), ('\n\n + '
'\n\n', )]forold, newinreplacements
rest_of_code = rest_of_code.replace(old, new)rest_of_code = re.sub('([{\\[] * '
'\\1', , rest_of_code)rest_of_code = re.sub' * [}\\]]'
'\\1', , rest_of_code)rest_of_code = re.sub(' * , * '
'
', , rest_of_code)rest_of_code = re.sub(', *
* '
'
', , rest_of_code)rest_of_code = re.sub(' *  =  * '
' = ', , rest_of_code)rest_of_code = re.sub(' * [ + \\ -  *  /  <  >  =  ! ] * '
'\\1', , rest_of_code)rest_of_code = re.sub('\\s + \\n'
'\\n', , rest_of_code)rest_of_code = re.sub('\\n\\s + '
'\\n', , rest_of_code)rest_of_code = re.sub('\\n{3, }'
'\\n\\n', , rest_of_code)word_fixes = [('in\\s + g'
'ing', ), ('or\\s + t'
'ort', ), ('f\\s + or'
'for', ), ('s\\s + or\\s + t'
'sort', ), ('cont\\s + in\\s + ue'
'continue', ), ('imp\\s + or\\s + t'
'import', ), ('doma\\s + in'
'domain', ), ('operat\\s + or'
'operator', ), ('r\\s + and\\s + om'
'random', ), ('str\\s + in\\s + g'
'string', ), ('typ\\s + in\\s + g'
'typing', ), ('is\\s + in\\s + stance'
'isinstance', ), ('m\\s + in'
'min', ), ('t\\s + or\\s + ch'
'torch', ), ('tens\\s + or\\s + flow'
'tensorflow', ), ('p\\s + and\\s + as'
'pandas', )]forpattern, replacementinword_fixes
rest_of_code = re.sub(pattern, replacement, rest_of_code)rest_of_code = re.sub('\\$\\w + \\s *  = \\s * ([pow, \\n] + )'
'\\1 = \\2', , rest_of_code)rest_of_code = re.sub('\\$\\w + '
'"\\1"', , rest_of_code)rest_of_code = re.sub('\\w + \\s *  = \\s * \\{[pow}] + \\}', lambdam
f'{m.group1} = {{\n{m.group2.strip}\n}}', rest_of_code)rest_of_code = re.sub('"[pow"] + "\\s * , \\s * "[pow"] + "'
'"\\1"
"\\2", ', , rest_of_code)rest_of_code = re.sub("\\'[pow\\'] + \\'\\s * , \\s * \\'[pow\\'] + \\'"
"'\\1'
'\\2', ", , rest_of_code)rest_of_code = re.sub('\\w + \\s *  = \\s * \\{[pow}] + \\}', lambdam
f'{m.group1} = {{\n{m.group2.strip}\n}}', rest_of_code)rest_of_code = re.sub('\\w + \\s *  = \\s * "[pow"] + "'
'\\1 = "\\2"', , rest_of_code)rest_of_code = re.sub("\\w + \\s *  = \\s * \\'[pow\\'] + \\'"
"\\1 = '\\2'", , rest_of_code)ifnotconfig.minify
lines = rest_of_code.split'\n'indent_level = 0indented_lines = []forlineinlines
line = line.stripifline.endswith'
'
indented_lines.append'' * indent_level + lineindent_level +  = 1eliflinein['}'
']', , ')']
indent_level = max(0, indent_level - 1)indented_lines.append'' * indent_level + lineelifline.startswith(('else
'
'elif', , 'except
'
'finally
', ))
indent_level = max(0, indent_level - 1)indented_lines.append'' * indent_level + lineindent_level +  = 1else
indented_lines.append'' * indent_level + linerest_of_code = '\n'.joinindented_linespython_code +  = rest_of_codereturnpython_codeexceptExceptionase
logger.error('ErrorconvertingPhitoncode
%s', stre)msg = f'InvalidPhitoncode
{e ! s}'raiseValueErrormsg⟩nextdefcalculate_stats(source: (str), result: (str)): (dict[(str, intBitOrfloat)])⟨'Calculatecompressionstatistics.\n\nArgs
\nsource
OriginalPythoncode\nresult
ConvertedPhitoncode\n\nReturns
\nDictionarywithcompressionstatistics\n'nextreturn{"original_chars"
lensource, "compressed_chars"
lenresult, "original_lines"
len(source.splitlines()), "compressed_lines"
len(result.splitlines()), "compression_ratio"
round(lenresult / lensource * #100, #2)}⟩nextdefprint_stats(report: (dict[(str, intBitOrfloat)])): (None)⟨'Printcompressionstatistics.'nextprint'\nCompressionStatistics
'nextprintf'Originalcharacters
{report['original_chars']}'nextprintf'Compressedcharacters
{report['compressed_chars']}'nextprintf'Originallines
{report['original_lines']}'nextprintf'Compressedlines
{report['compressed_lines']}'nextprintf'Compressionratio
{report['compression_ratio']}%'⟩nextdefconvert(decompress: (bool), report: (bool), level: (int), comments: (bool), type_hints: (bool), minify: (bool), symbols: (bool), input_path: (strBitOrPathBitOrNone), output_path: (strBitOrPathBitOrNone), verbose: (bool)): (None)⟨"ConvertbetweenPythonandPhitonnotation.\n\nArgs
\ninput_path
input_pathfilepathor' - 'forstdin\noutput_path
output_pathfilepathor' - 'forstdout\ndecompress
IfTrue, convertfromPhitontoPython\nreport
Showcompressionstatistics\nlevel
Compressionlevel1 - 5\ncomments
Whethertopreservecommentsinoutput_path\ntype_hints
Whethertoincludetypehintsinoutput_path\nminify
Whethertocompresswhitespace\nsymbols
Whethertouselocalsymboloptimization\nverbose
Enableverboselogging\n"nextlogger.remove()nextlogger.add(sys.stderr, level = 'DEBUG'ifverboseelse'INFO')nexttry
ifinput_pathisNoneorinput_path =  = ' - '
logger.debug'Readingfromstdin...'source_code = sys.stdin.read()else
input_path = Pathinput_pathifnotinput_path.exists()
msg = f'input_pathfilenotfound
{input_path}'raiseFileNotFoundErrormsglogger.debugf'Readingfrom{input_path}...'source_code = input_path.read_textencoding = 'utf - 8'conv_config = ConversionConfig(level = level, comments = comments, type_hints = type_hints, minify = minify, symbols = symbols)ifdecompress
logger.debug'DecompressingPhitontoPython...'result_code = decompress_from_phiton(source_code, conv_config)operation = 'decompressed'else
logger.debug'CompressingPythontoPhiton...'result_code = compress_to_phiton(source_code, conv_config)operation = 'compressed'ifoutput_pathisNoneoroutput_path =  = ' - '
logger.debug'Writingtostdout...'sys.stdout.writeresult_codeelse
output_path = Pathoutput_pathlogger.debugf'Writingto{output_path}...'output_path.write_text(result_code, encoding = 'utf - 8')ifreportandoperation =  = 'compressed'
stats_data = calculate_stats(source_code, result_code)print_statsstats_datalogger.debugf'Successfully{operation}code'exceptExceptionase
logger.errorf'Error
{e ! s}'sys.exit1⟩nextdefmain(): (None)⟨'Mainentrypointforphiton.'nexttry
fire.FireconvertexceptExceptionase
logger.errorf'Error
{e ! s}'sys.exit1⟩nextif__name__ =  = "__main__"⟨main()⟩