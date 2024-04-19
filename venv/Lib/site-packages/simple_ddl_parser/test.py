from simple_ddl_parser import DDLParser

ddl = """
CREATE TABLE tablename ();

"""
result = DDLParser(ddl).run(group_by_type=True, 
                            output_mode="mysql")

import pprint

pprint.pprint(result)