'abstract'      : flattenBoolean
'access'        :
'alias'         : flattenName
'arg'           : synonym('param')
'argument'      : synonym('param')
'augments'      :
'author'        : flattenDescription
'borrows'       : todo
'callback'      :
'class'         : flattenKindShorthand
'classdesc'     : flattenMarkdownDescription
'const'         : synonym('constant')
'constant'      : flattenKindShorthand
'constructor'   : synonym('class')
'constructs'    : todo
'copyright'     : flattenMarkdownDescription
'default'       : todo
'defaultvalue'  : synonym('default')
'deprecated'    : flattenMarkdownDescription
'desc'          : synonym('description')
'description'   : flattenMarkdownDescription
'emits'         : synonym('fires')
'enum'          : todo
'event'         :
'example'       :
'exception'     : synonym('throws')
'exports'       : todo
'extends'       : synonym('augments')
'external'      :
'file'          :
'fileoverview'  : synonym('file')
'fires'         : todo
'func'          : synonym('function')
'function'      : flattenKindShorthand
'global'        :
'host'          : synonym('external')
'ignore'        : flattenBoolean
'implements'    : todo
'inheritdoc'    : todo
'inner'         :
'instance'      :
'interface'     :
'kind'          :
'lends'         : flattenDescription
'license'       : flattenDescription
'listens'       : todo
'member'        : flattenKindShorthand
'memberof'      : flattenDescription
'method'        : synonym('function')
'mixes'         : todo
'mixin'         : flattenKindShorthand
'module'        : flattenKindShorthand
'name'          : flattenName
'namespace'     : flattenKindShorthand
'override'      : flattenBoolean
'overview'      : synonym('file')
'param'         :
'private'       :
'prop'          : synonym('property')
'property'      :
'protected'     :
'public'        :
'readonly'      : flattenBoolean
'requires'      : todo
'return'        : synonym('returns')
'returns'       :
'see'           :
'since'         : flattenDescription
'static'        :
'summary'       : flattenMarkdownDescription
'this'          : todo
'throws'        :
'todo'          :
'tutorial'      : todo
'type'          : todo
'typedef'       : flattenKindShorthand
'var'           : synonym('member')
'variation'     :
'version'       : flattenDescription
'virtual'       : synonym('abstract')
