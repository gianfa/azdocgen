<!-- markdownlint-disable MD024 -->
# User Guide: Enriching Azure Pipelines YAML for AZDocGen

AZDocGen supports extracting documentation directly embedded in Azure Pipelines YAML files. You can add metadata, descriptions, and conditions to make your pipeline more informative and easier to understand.

## Contents

- [Contents](#contents)
- [1. Metadata Section (Header Documentation)](#1-metadata-section-header-documentation)
  - [Supported Tags](#supported-tags)
  - [Example](#example)
- [2. Adding Descriptions to Steps and Jobs](#2-adding-descriptions-to-steps-and-jobs)
  - [For Steps](#for-steps)
    - [Example](#example-1)
  - [For Jobs](#for-jobs)
    - [Example](#example-2)
- [3. Documenting Conditions](#3-documenting-conditions)
  - [Supported Formats](#supported-formats)
- [4. Using Templates](#4-using-templates)
  - [Example](#example-3)
- [5. Example Enriched Pipeline YAML](#5-example-enriched-pipeline-yaml)
- [Tips for Effective Documentation](#tips-for-effective-documentation)

## 1. Metadata Section (Header Documentation)

Add a header at the beginning of the YAML file to include high-level metadata about the pipeline. Use tags prefixed with `#` and starting with `@`.

### Supported Tags

- `@title`: Title of the pipeline.
- `@description`: A brief description of the pipeline's purpose or functionality.
- `@author`: Author or team responsible for the pipeline.
- `@version`: Version of the pipeline.

### Example

```yaml
# @title: CI/CD Pipeline
# @description: This pipeline automates the build, test, and deploy process
#   for our application, ensuring high-quality releases.
# @author: DevOps Team
# @version: 2.1

# Then your code follows
trigger:
  batch: "true"
  branches:
    include:
      - '*'
# ...
```

## 2. Adding Descriptions to Steps and Jobs

Each step and job can have a `displayName` or `name` field, which AZDocGen extracts to generate documentation.

### For Steps

- Use the `displayName` field to describe the action being performed.
- If a `displayName` is not provided, the script, template, or checkout type will be used.

#### Example

```yaml
steps:
  - script: echo "Building application"
    displayName: "Build the Application"
  - script: echo "Running tests"
    displayName: "Run Unit Tests"
```

### For Jobs

- Add a `displayName` to describe the job's purpose.

#### Example

```yaml
jobs:
  - job: Build
    displayName: "Build the Application"
    steps:
      - script: npm install
      - script: npm run build
```

## 3. Documenting Conditions

Conditions can be global or local (within jobs or steps). You can document these conditions by using standard YAML `condition` fields or inline conditions.

### Supported Formats

1. **Global Conditions**:  
   Use the `condition` field for stages or jobs.

    ```yaml
    - stage: Deploy
        displayName: "Deploy Stage"
        condition: eq(variables['Build.SourceBranch'], 'refs/heads/main')
    ```

2. **Inline Conditions**:  
   Use the `${{ if }}` syntax within steps or jobs.

    ```yaml
    steps:
        - ${{ if eq(variables['Build.SourceBranch'], 'refs/heads/main') }}:
            script: echo "Deploying to production"
    ```

## 4. Using Templates

When reusing templates in your pipeline, make sure the template names are descriptive.

### Example

```yaml
steps:
  - template: build-template.yml
    parameters:
      environment: production
```

## 5. Example Enriched Pipeline YAML

Here’s an example of a pipeline YAML enriched with documentation:

```yaml
# @title: Comprehensive CI/CD Pipeline
# @description: Automates building, testing, and deploying a microservice.
#   Includes conditional deployment and reusable templates.
# @author: DevOps Team
# @version: 1.0

trigger:
  branches:
    include:
      - main

resources:
  repositories:
    - repository: shared-templates
      type: git
      name: org/shared-templates

stages:
  - stage: Build
    displayName: "Build Stage"
    condition: eq(variables['Build.SourceBranch'], 'refs/heads/main')
    jobs:
      - job: BuildApp
        displayName: "Build the Application"
        pool:
          vmImage: "ubuntu-latest"
        steps:
          - script: echo "Compiling application..."
            displayName: "Compile App"
          - script: echo "Packaging application..."
            displayName: "Package App"

  - stage: Deploy
    displayName: "Deploy Stage"
    dependsOn: Build
    condition: eq(variables['Build.SourceBranch'], 'refs/heads/main')
    jobs:
      - job: DeployToProd
        displayName: "Deploy to Production"
        steps:
          - ${{ if eq(variables['Environment'], 'Production') }}:
              script: echo "Deploying to production"
              displayName: "Deploy Production Environment"
```

## Tips for Effective Documentation

1. **Be Consistent**:  
   Use `displayName` for all steps and jobs to ensure clarity in what each action performs.

2. **Use Metadata**:  
   Always include a header at the top of your YAML file with tags such as `@title`, `@description`, `@author`, and `@version` to provide context.

3. **Leverage Templates**:  
   Use meaningful names and parameters in templates to make your pipeline more reusable and comprehensible.

By following these tips, your Azure Pipelines YAML will be easier to maintain, understand, and document effectively with AZDocGen.
