# Schema Validator

> [!NOTE]
> Support JSON, YAML, TOML, and XML. I have plans to add functionality to validate .env files as well.

- [![Test Files - Full Schema Validation](https://github.com/chase-roohms/schema-validator/actions/workflows/test-schema-validation-files.yml/badge.svg)](https://github.com/chase-roohms/schema-validator/actions/workflows/test-schema-validation-files.yml)
- [![Test File Format - Full Schema Validation](https://github.com/chase-roohms/schema-validator/actions/workflows/test-schema-validation-file-format.yml/badge.svg)](https://github.com/chase-roohms/schema-validator/actions/workflows/test-schema-validation-file-format.yml)
- [![Test Input Validation](https://github.com/chase-roohms/schema-validator/actions/workflows/test-input-validation.yml/badge.svg)](https://github.com/chase-roohms/schema-validator/actions/workflows/test-input-validation.yml)
- [![Test Output File and Format](https://github.com/chase-roohms/schema-validator/actions/workflows/test-output-file.yml/badge.svg)](https://github.com/chase-roohms/schema-validator/actions/workflows/test-output-file.yml)
- [![Test Action Outputs](https://github.com/chase-roohms/schema-validator/actions/workflows/test-action-outputs.yml/badge.svg)](https://github.com/chase-roohms/schema-validator/actions/workflows/test-action-outputs.yml)

A flexible GitHub Action for validating JSON, YAML, and XML files against schemas. Supports both local schema files and remote schema URLs, with comprehensive validation reporting in JSON or text format.

### Quick Start

```yaml
- name: Checkout Repository
  uses: actions/checkout@v4

- name: Validate JSON Files
  uses: chase-roohms/schema-validator@v1
  with:
    files: |
      data/users.json
      data/products.json
      config/settings.json
    schema-file: schemas/api-schema.json
```


## Features

- **Multi-Format Support**: Validate JSON, YAML, TOML, and XML files
- **Flexible Schema Sources**: Use local schema files or remote URLs
- **Schema Compatibility**: JSON, YAML, and TOML schemas are interchangeable (all validate JSON/YAML/TOML files)
- **Multiple Output Formats**: Generate validation reports in JSON or text format
- **Selective Validation**: Validate specific files or scan entire repository
- **Built-in Pre-validation**: Automatic checks for file existence, format compatibility, and schema reachability
- **Detailed Error Reporting**: Comprehensive validation error messages
- **Composable**: Easy integration with other GitHub Actions (artifacts, notifications, etc.)

## Table of Contents

- [Inputs](#inputs)
- [Outputs](#outputs)
- [Usage Examples](#usage-examples)
  - [Basic Examples](#basic-examples)
  - [Validating Specific Files](#validating-specific-files)
  - [Auto-Discovery](#auto-discovery)
  - [Using Schema URLs](#using-schema-urls)
  - [XML Validation](#xml-validation)
  - [Output Formats](#output-formats)
  - [Advanced Examples](#advanced-examples)
- [Schema Format Compatibility](#schema-format-compatibility)
- [Error Handling](#error-handling)
- [License](#license)

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `files` | Newline-separated list of files to validate. If not provided, all files matching `file-format` will be validated. | No | - |
| `file-format` | Format of files to validate. Options: `json`, `yaml`, `toml`, `xml`. Required if `files` is not provided. Inferred from file extensions if `files` is provided. | No | - |
| `schema-file` | Path to local schema file. Must exist on the runner. Mutually exclusive with `schema-url`. | No¹ | - |
| `schema-url` | URL of the schema to validate against. Will be fetched and used for validation. Mutually exclusive with `schema-file`. | No¹ | - |
| `schema-format` | Format of the schema. Options: `json`, `yaml`, `toml`, `xml`. Will be inferred from file extension if not provided. | No | - |
| `output-format` | Format of validation results. Options: `json`, `text`. | No | `json` |
| `output-file` | Path to write validation results. | No | `${{ runner.temp }}/validation-results` |

¹ **Note**: Exactly one of `schema-file` or `schema-url` must be provided.

## Outputs

| Output | Description |
|--------|-------------|
| `validation-passed` | Boolean string (`"true"` or `"false"`) indicating whether all validations passed |
| `output-file` | Path to the file containing validation results |

## Usage Examples

### Basic Examples

#### Validate JSON Files Against JSON Schema

```yaml
- name: Checkout Repository
  uses: actions/checkout@v4

- name: Validate JSON Files
  uses: chase-roohms/schema-validator@v1
  with:
    files: |
      data/users.json
      data/products.json
      config/settings.json
    schema-file: schemas/api-schema.json
```

#### Validate YAML Files Against YAML Schema

```yaml
- name: Validate YAML Configuration
  uses: chase-roohms/schema-validator@v1
  with:
    files: |
      config/app.yaml
      config/database.yaml
    schema-file: schemas/config.schema.yaml
```

#### Validate TOML Files Against TOML Schema

```yaml
- name: Checkout Repository
  uses: actions/checkout@v4

- name: Validate TOML Files
  uses: chase-roohms/schema-validator@v1
  with:
    files: |
      data/users.toml
      data/products.toml
      config/settings.toml
    schema-file: schemas/api-schema.toml
```

#### Validate Mixed JSON/YAML Files

Since JSON and YAML schemas are interchangeable, you can validate both formats with a single schema:

```yaml
- name: Validate Configuration Files
  uses: chase-roohms/schema-validator@v1
  with:
    files: |
      config/prod.json
      config/dev.yaml
      config/staging.yml
    schema-file: schemas/config.schema.json
```

### Validating Specific Files

#### Single File Validation

```yaml
- name: Validate API Response
  uses: chase-roohms/schema-validator@v1
  with:
    files: api-response.json
    schema-file: schemas/api.schema.json
```

#### Multiple Files from Different Directories

```yaml
- name: Validate Data Files
  uses: chase-roohms/schema-validator@v1
  with:
    files: |
      src/data/users.json
      tests/fixtures/mock-data.json
      docs/examples/sample.json
    schema-file: schemas/data.schema.json
```

### Auto-Discovery

Let the action find all files of a specific format in your repository:

#### Find and Validate All JSON Files

```yaml
- name: Validate All JSON Files
  uses: chase-roohms/schema-validator@v1
  with:
    file-format: json
    schema-file: schemas/any.schema.json
```

#### Find and Validate All YAML Files

```yaml
- name: Validate All YAML Files
  uses: chase-roohms/schema-validator@v1
  with:
    file-format: yaml
    schema-file: schemas/config.schema.yaml
```

#### Find and Validate All XML Files

```yaml
- name: Validate All XML Files
  uses: chase-roohms/schema-validator@v1
  with:
    file-format: xml
    schema-file: schemas/document.xsd
```

### Using Schema URLs

Fetch schemas from remote sources:

#### GitHub Raw Content

```yaml
- name: Validate Against Remote Schema
  uses: chase-roohms/schema-validator@v1
  with:
    files: data/users.json
    schema-url: https://raw.githubusercontent.com/org/schemas/main/user.schema.json
```

#### JSON Schema Store

```yaml
- name: Validate Package.json
  uses: chase-roohms/schema-validator@v1
  with:
    files: package.json
    schema-url: https://json.schemastore.org/package.json
```

#### Organization Schema Registry

```yaml
- name: Validate Configuration
  uses: chase-roohms/schema-validator@v1
  with:
    files: config.yaml
    schema-url: https://schemas.example.com/v1/config.schema.json
```

### XML Validation

XML validation uses XSD (XML Schema Definition):

#### Validate XML Files

```yaml
- name: Validate XML Documents
  uses: chase-roohms/schema-validator@v1
  with:
    files: |
      data/document1.xml
      data/document2.xml
    schema-file: schemas/document.xsd
```

#### Validate All XML Files in Repository

```yaml
- name: Validate All XML
  uses: chase-roohms/schema-validator@v1
  with:
    file-format: xml
    schema-file: schemas/standard.xsd
```

### Output Formats

#### JSON Output (Default)

```yaml
- name: Validate with JSON Output
  uses: chase-roohms/schema-validator@v1
  with:
    files: data/users.json
    schema-file: schemas/user.schema.json
    output-format: json
    output-file: validation-results.json
```

Example JSON output:
```json
{
  "test-files/json/good_1.json": {
    "passed": true,
    "notes": ""
  },
  "test-files/json/good_2.json": {
    "passed": true,
    "notes": ""
  },
  "test-files/json/good_3.json": {
    "passed": true,
    "notes": ""
  }
}
```

#### Text Output

```yaml
- name: Validate with Text Output
  uses: chase-roohms/schema-validator@v1
  with:
    files: data/users.json
    schema-file: schemas/user.schema.json
    output-format: text
    output-file: validation-results.txt
```

Example text output:
```
test-files/yaml/bad_1.yaml: not valid
-5 is less than the minimum of 0

Failed validating 'minimum' in schema['properties']['age']:
    {'type': 'integer', 'minimum': 0, 'maximum': 150}

On instance['age']:
    -5

test-files/yaml/bad_2.yaml: not valid
200 is greater than the maximum of 150

Failed validating 'maximum' in schema['properties']['age']:
    {'type': 'integer', 'minimum': 0, 'maximum': 150}

On instance['age']:
    200

```

### Advanced Examples

#### Upload Validation Results as Artifact

```yaml
- name: Validate Files
  id: validate
  uses: chase-roohms/schema-validator@v1
  continue-on-error: true
  with:
    files: |
      data/file1.json
      data/file2.json
    schema-file: schemas/data.schema.json
    output-format: json
    output-file: ${{ runner.temp }}/validation-results.json

- name: Upload Validation Results
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: validation-results
    path: ${{ steps.validate.outputs.output-file }}
```

#### Conditional Steps Based on Validation

```yaml
- name: Validate Configuration
  id: validate-config
  uses: chase-roohms/schema-validator@v1
  continue-on-error: true
  with:
    files: config/production.yaml
    schema-file: schemas/config.schema.yaml

- name: Deploy to Production
  if: steps.validate-config.outputs.validation-passed == 'true'
  run: |
    echo "Configuration is valid, deploying..."
    # deployment steps here

- name: Notify on Failure
  if: steps.validate-config.outputs.validation-passed == 'false'
  run: |
    echo "Configuration validation failed!"
    cat ${{ steps.validate-config.outputs.output-file }}
```

#### Send Validation Report via Slack

```yaml
- name: Validate API Schemas
  id: validate-schemas
  uses: chase-roohms/schema-validator@v1
  continue-on-error: true
  with:
    file-format: json
    schema-file: schemas/api.schema.json
    output-format: text
    output-file: validation-report.txt

- name: Send Report to Slack
  if: always()
  uses: slackapi/slack-github-action@v1
  with:
    payload: |
      {
        "text": "Schema Validation Results",
        "attachments": [{
          "color": "${{ steps.validate-schemas.outputs.validation-passed == 'true' && 'good' || 'danger' }}",
          "text": "${{ steps.validate-schemas.outputs.validation-passed == 'true' && 'All validations passed ✅' || 'Validation failed ❌' }}"
        }]
      }
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

#### Create GitHub Issue on Validation Failure

```yaml
- name: Validate Data Files
  id: validate
  uses: chase-roohms/schema-validator@v1
  continue-on-error: true
  with:
    file-format: json
    schema-file: schemas/data.schema.json
    output-format: text
    output-file: validation-results.txt

- name: Read Validation Results
  if: steps.validate.outputs.validation-passed == 'false'
  id: results
  run: echo "results=$(cat validation-results.txt)" >> $GITHUB_OUTPUT

- name: Create Issue
  if: steps.validate.outputs.validation-passed == 'false'
  uses: actions/github-script@v7
  with:
    script: |
      await github.rest.issues.create({
        owner: context.repo.owner,
        repo: context.repo.repo,
        title: 'Schema Validation Failed',
        body: `Schema validation failed in workflow ${context.workflow}.\n\n\`\`\`\n${{ steps.results.outputs.results }}\n\`\`\``,
        labels: ['validation-failure', 'automated']
      });
```

#### Matrix Strategy with Multiple Schemas

```yaml
jobs:
  validate:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        environment: [dev, staging, prod]
        include:
          - environment: dev
            schema: schemas/dev.schema.json
          - environment: staging
            schema: schemas/staging.schema.json
          - environment: prod
            schema: schemas/prod.schema.json
    steps:
      - uses: actions/checkout@v4
      
      - name: Validate ${{ matrix.environment }} Config
        uses: chase-roohms/schema-validator@v1
        with:
          files: config/${{ matrix.environment }}.json
          schema-file: ${{ matrix.schema }}
```

#### Pull Request Comment with Results

```yaml
- name: Validate Changes
  id: validate
  uses: chase-roohms/schema-validator@v1
  continue-on-error: true
  with:
    files: |
      modified-file1.json
      modified-file2.json
    schema-file: schemas/api.schema.json
    output-format: text
    output-file: validation.txt

- name: Comment PR
  if: github.event_name == 'pull_request'
  uses: actions/github-script@v7
  with:
    script: |
      const fs = require('fs');
      const results = fs.readFileSync('validation.txt', 'utf8');
      const passed = '${{ steps.validate.outputs.validation-passed }}' === 'true';
      const emoji = passed ? '✅' : '❌';
      
      await github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body: `${emoji} **Schema Validation Results**\n\n\`\`\`\n${results}\n\`\`\``
      });
```

#### Validate Generated Files from Previous Step

```yaml
- name: Generate Configuration
  run: |
    # Script that generates config files
    ./scripts/generate-config.sh

- name: Validate Generated Files
  uses: chase-roohms/schema-validator@v1
  with:
    file-format: json
    schema-file: schemas/generated-config.schema.json
```

#### Multi-Stage Validation Pipeline

```yaml
jobs:
  validate-dev:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate Dev Configs
        uses: chase-roohms/schema-validator@v1
        with:
          files: |
            config/dev/app.json
            config/dev/database.json
            config/dev/services.json
          schema-file: schemas/dev.schema.json

  validate-prod:
    runs-on: ubuntu-latest
    needs: validate-dev
    steps:
      - uses: actions/checkout@v4
      - name: Validate Prod Configs
        uses: chase-roohms/schema-validator@v1
        with:
          files: |
            config/prod/app.json
            config/prod/database.json
            config/prod/services.json
          schema-file: schemas/prod.schema.json
          
  deploy:
    runs-on: ubuntu-latest
    needs: [validate-dev, validate-prod]
    steps:
      - name: Deploy Application
        run: echo "All validations passed, deploying..."
```

## Schema Format Compatibility

The action enforces schema format compatibility:

### ✅ Compatible Combinations

- **JSON Schema** → JSON files
- **JSON Schema** → YAML files
- **JSON Schema** → Mixed JSON/YAML files
- **YAML Schema** → JSON files
- **YAML Schema** → YAML files
- **YAML Schema** → Mixed JSON/YAML files
- **XSD Schema** → XML files only

### ❌ Incompatible Combinations

- **XSD Schema** → JSON files *(will fail)*
- **XSD Schema** → YAML files *(will fail)*
- **JSON/YAML Schema** → XML files *(will fail)*

**Why?** JSON and YAML use the same schema format (JSON Schema), so they're interchangeable. XML uses a different schema system (XSD), which is incompatible with JSON/YAML.

## Error Handling

The action includes comprehensive validation checks:

### Pre-validation Checks

- Repository checkout verification
- File existence validation
- Schema file/URL accessibility
- Format compatibility checks
- Input parameter validation

### Validation Failures

When validation fails:
- The action will exit with code 1
- `validation-passed` output will be `"false"`
- Error details will be written to the output file
- Use `continue-on-error: true` to prevent workflow failure

Example:
```yaml
- name: Validate Files
  id: validate
  uses: chase-roohms/schema-validator@v1
  continue-on-error: true  # Don't fail the workflow
  with:
    files: data.json
    schema-file: schema.json

- name: Handle Validation Failure
  if: steps.validate.outputs.validation-passed == 'false'
  run: |
    echo "Validation failed, but workflow continues"
    cat ${{ steps.validate.outputs.output-file }}
```

## Requirements

- Repository must be checked out (use `actions/checkout` before this action)
- Schema file must exist if using `schema-file`
- Schema URL must be accessible if using `schema-url`

## License

This action is available under the MIT License. See [LICENSE](LICENSE) for details.

---

**Author**: Chase Roohms

**Issues and Contributions**: Visit the [GitHub repository](https://github.com/chase-roohms/schema-validator) to report issues or contribute.
