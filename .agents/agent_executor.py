#!/usr/bin/env python3
"""Simple Documentation Generator Executor

Usage:
  python .agents/agent_executor.py --module mailer.subscribers [--output docs] [--run-tests]

This script parses a Python module file, extracts module/class/function
signatures and docstrings, and writes basic Markdown documentation.
"""
import argparse
import ast
import os
import sys
from typing import List, Tuple


def find_module_path(module: str) -> str:
    path = module.replace('.', os.sep) + '.py'
    if os.path.exists(path):
        return path
    pkg_init = os.path.join(module.replace('.', os.sep), '__init__.py')
    if os.path.exists(pkg_init):
        return pkg_init
    return ''


def unparse_annotation(node):
    try:
        return ast.unparse(node)
    except Exception:
        return ''


def extract_api(file_path: str) -> Tuple[str, List[dict], List[dict]]:
    with open(file_path, 'r', encoding='utf-8') as f:
        src = f.read()
    mod = ast.parse(src)
    module_doc = ast.get_docstring(mod) or ''
    functions = []
    classes = []
    for node in mod.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            name = node.name
            args = []
            for arg in node.args.args:
                anno = unparse_annotation(arg.annotation) if arg.annotation else ''
                args.append((arg.arg, anno))
            returns = unparse_annotation(node.returns) if node.returns else ''
            doc = ast.get_docstring(node) or ''
            functions.append({
                'name': name,
                'args': args,
                'returns': returns,
                'doc': doc,
            })
        elif isinstance(node, ast.ClassDef):
            cls_name = node.name
            cls_doc = ast.get_docstring(node) or ''
            methods = []
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if item.name.startswith('__') and item.name.endswith('__'):
                        continue
                    m_args = []
                    # skip self
                    for arg in item.args.args[1:]:
                        anno = unparse_annotation(arg.annotation) if arg.annotation else ''
                        m_args.append((arg.arg, anno))
                    m_returns = unparse_annotation(item.returns) if item.returns else ''
                    m_doc = ast.get_docstring(item) or ''
                    methods.append({
                        'name': item.name,
                        'args': m_args,
                        'returns': m_returns,
                        'doc': m_doc,
                    })
            classes.append({'name': cls_name, 'doc': cls_doc, 'methods': methods})
    return module_doc, functions, classes


def format_signature(name: str, args: List[Tuple[str,str]], returns: str) -> str:
    args_formatted = ', '.join([f"{n}: {a}" if a else n for n,a in args])
    sig = f"def {name}({args_formatted})"
    if returns:
        sig += f" -> {returns}"
    return sig


def generate_markdown(module: str, module_doc: str, functions: List[dict], classes: List[dict]) -> str:
    lines = []
    lines.append(f"# API: {module}")
    lines.append('')
    if module_doc:
        lines.append(module_doc)
        lines.append('')
    if functions:
        lines.append('## Functions')
        lines.append('')
        for fn in functions:
            lines.append(f"### {fn['name']}")
            lines.append('')
            lines.append('```python')
            lines.append(format_signature(fn['name'], fn['args'], fn['returns']))
            lines.append('```')
            lines.append('')
            if fn['doc']:
                lines.append(fn['doc'])
                lines.append('')
    if classes:
        lines.append('## Classes')
        lines.append('')
        for cl in classes:
            lines.append(f"### {cl['name']}")
            lines.append('')
            if cl['doc']:
                lines.append(cl['doc'])
                lines.append('')
            for m in cl['methods']:
                lines.append(f"#### {m['name']}")
                lines.append('')
                lines.append('```python')
                lines.append(format_signature(m['name'], m['args'], m['returns']))
                lines.append('```')
                lines.append('')
                if m['doc']:
                    lines.append(m['doc'])
                    lines.append('')
    # Examples placeholder
    lines.append('## Examples')
    lines.append('')
    lines.append('Basic usage example to be filled in by the agent.')
    lines.append('')
    return '\n'.join(lines)


def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--module', required=True, help='Target module (dot path) or file')
    parser.add_argument('--output', default='docs', help='Output docs directory')
    parser.add_argument('--run-tests', action='store_true', help='Run pytest after generation')
    args = parser.parse_args()

    module = args.module
    # if module is a file path
    if os.path.isfile(module):
        file_path = module
        module_name = os.path.splitext(os.path.basename(file_path))[0]
    elif os.path.isdir(module):
        init_path = os.path.join(module, '__init__.py')
        if os.path.exists(init_path):
            file_path = init_path
            module_name = module.replace(os.sep, '.')
        else:
            print(f"ERROR: Directory '{module}' is not a Python package (no __init__.py)")
            sys.exit(2)
    else:
        file_path = find_module_path(module)
        module_name = module

    if not file_path:
        print(f"ERROR: Could not find module file for '{module}'. Checked '{module.replace('.', os.sep)}.py'")
        sys.exit(2)

    print(f"Parsing {file_path} ...")
    module_doc, functions, classes = extract_api(file_path)

    out_api_dir = os.path.join(args.output, 'api')
    out_examples_dir = os.path.join(args.output, 'examples')
    ensure_dir(out_api_dir)
    ensure_dir(out_examples_dir)

    md = generate_markdown(module, module_doc, functions, classes)
    out_file = os.path.join(out_api_dir, f"{module.replace('.', '_')}.md")
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(md)
    print(f"Wrote API docs to {out_file}")

    example_file = os.path.join(out_examples_dir, f"{module.replace('.', '_')}_usage.md")
    with open(example_file, 'w', encoding='utf-8') as f:
        f.write('# Examples for ' + module + '\n\n')
        f.write('To be implemented.\n')
    print(f"Wrote examples to {example_file}")

    if args.run_tests:
        print('Running pytest...')
        import subprocess
        subprocess.run([sys.executable, '-m', 'pytest', '-q'])


if __name__ == '__main__':
    main()
