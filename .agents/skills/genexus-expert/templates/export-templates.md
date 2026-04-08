# Nexa Object Template (Markdown)

```yaml
nexa_object:
  name: [ObjectName]
  type: [Transaction|Procedure|DataProvider|API|Panel]
  namespace: [Module.General]
  description: [Clear description]
  structure:
    - name: [AttributeName]
      type: [numeric|varchar|datetime|...]
      id: [true|false]
  logic:
    rules:
      - [GxRule]
    events:
      - [GxEvent]
    commands:
      - [GxCommand]
```

# GeneXus Import Template (YAML)

```yaml
# GX18/Next Compatible Import
gx_import:
  version: 1.0
  objects:
    - name: [ObjectName]
      type: [Transaction]
      description: [Description]
      definition:
        attributes:
          - [AttributeDetails]
        rules: |
          [RawRules]
        events: |
          [RawEvents]
```
