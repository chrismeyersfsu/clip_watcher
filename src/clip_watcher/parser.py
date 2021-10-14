#!/usr/bin/env python3

import astor
import ast
import json


def do_parse_json(json_file_path):
    data = open(json_file_path).read()
    jd = json.loads(data)


def do_build_ast_to_parse_json(json_file_path):
    data = open(json_file_path).read()
    jd = json.loads(data)

    #start_func = astor.code_to_ast(do_parse_json)

    for_target_kv = ast.Tuple([ast.Name('root_k', ast.Store()), ast.Name('root_v', ast.Store()), ast.Store()])
    root_loop = ast.For(for_target_kv,
                        ast.Name('jd', ast.Load()))

    return root_loop


ast_to_parse_json = do_build_ast_to_parse_json('sample.json')

s = astor.to_source(ast_to_parse_json)
print(s)
