# Script version definition, conforms to the SemiVer standard
script_ver = 100

import understand
import argparse
import json
import sys
import re

# Usage
parser = argparse.ArgumentParser()
parser.add_argument('db', help='Specify Understand database name')
parser.add_argument('out', help='Specify output file\'s name and location')
parser.add_argument('-p', help='Print mode, only print final JSON string',
    action=argparse.BooleanOptionalAction)
args = parser.parse_args()

print_mode = args.p


def contain(keyword, raw):
    return bool(re.search(r'(^| )%s' % keyword, raw))


if __name__ == '__main__':
    und_ver = understand.version()

    if not print_mode:
        print('Opening udb file...')
    db = understand.open(args.db)

    ent_list = []

    # Extract file entities first
    if not print_mode:
        print('Exporting File entities...')
    file_count = 0
    for ent in db.ents('File'):
        if ent.language() == 'Python' and ent.library() != 'Standard':
#           if 'SciTools' not in ent.relname():
            ent_list.append({
                'id': ent.id(),
                'type': 'File',
                # Relative name
                'name': ent.relname(),
            })
            file_count += 1
    for ent in db.ents('Package'):
        if ent.language() == 'Python' and ent.library() != 'Standard':
            ent_list.append({
                'id': ent.id(),
                'type': 'Package',
                'name': ent.name(),
                'qualified_name': ent.longname(),
            })
    if not print_mode:
        print(f'Total {file_count} files are successfully exported')

    if not print_mode:
        print('Exporting entities other that File...')
    regular_count = 0

    # Filter entities other than file
    for ent in db.ents('~File ~Package ~Unknown ~Ambiguous ~Unresolved ~Predefined'):
        if ent.language() == 'Python' and ent.library() != 'Standard':
            # Although a suffix 's' is added, there should be only
            # one entry that matches the condition
            decls = ent.refs('Definein')
            if decls and 'SciTools' not in decls[0].file().relname():
                # Normal entities should have a ref definein contains location
                # about where this entity is defined
                line = decls[0].line()
                start_column = decls[0].column() + 1
                end_column = start_column + len(ent.simplename())
                ent_list.append({
                    'id': ent.id(),
                    'type': ent.kind().longname(),
                    'name': ent.name(),
                    'qualified_name': ent.longname(),
                    'line': line,
                    'start_column': start_column,
                    'end_column': end_column,
                    'belongs_to': decls[0].file().id(),
                })
                regular_count += 1
            else:
                ent_list.append({
                    'id': ent.id(),
                    'type': ent.kind().longname(),
                    'name': ent.name(),
                    'qualified_name': ent.longname(),
                    'line': -1,
                    'start_column': -1,
                    'end_column': -1,
                })

    all_ent_kinds = set()
    for ent in ent_list:
        all_ent_kinds.add(ent['type'])

    rel_list = []

    if not print_mode:
        print('Exporting relations...')
    rel_count = 0
    for ent in db.ents():
        if ent.language() == 'Python' and ent.library() != 'Standard':
            for ref in ent.refs('~End', '~Unknown ~Unresolved ~Implicit ~Ambiguous ~Predefined'):
                if ref.isforward():
                    rel_list.append({
                        'from': ref.scope().id(),
                        'to': ref.ent().id(),
                        # Using kind().longname() rather than kindname() to acquire longname
                        # in case meeting `Pointer` instead of `Use Ptr`
                        'type': ref.kind().longname(),
                        'inFile': ref.file().id(),
                        'line': ref.line(),
                        'column': ref.column() + 1,
                    })
                    rel_count += 1

    all_rel_kinds = set()
    for rel in rel_list:
        all_rel_kinds.add(rel['type'])

    struct = {
        'script_ver': script_ver,
        'und_ver': und_ver,
        'db_name': args.db,
        'entities': ent_list,
        'relations': rel_list,
    }
    if print_mode:
        print(json.dumps(struct))
    else:
        print('Saving results to the file...')
        with open(args.out, 'w') as out:
            json.dump(struct, out, indent=4)
        print(f'Total {regular_count} entities and {rel_count} relations are successfully exported')
        print('All possible entity types are', sorted(all_ent_kinds))
        print('All possible relation types are', sorted(all_rel_kinds))
