# n8n Workflow Nodes Database

This repository stores comprehensive information about n8n workflow nodes, optimized for querying and integration with n8n automation systems.

## Database Structure

The database is a single JSON file located at `nodes/db.json`. Each object in the JSON array represents a single n8n node and contains the following fields:

-   `node_type` (String): The unique identifier for the node type (e.g., `"nodes-base.webhook"`).
-   `package_name` (String): The npm package name (e.g., `"n8n-nodes-base"`).
-   `display_name` (String): Human-readable name (e.g., `"Webhook"`).
-   `description` (String): A brief summary of the node's purpose.
-   `category` (String): The node category (e.g., `"trigger"`, `"action"`, `"ai"`).
-   `development_style` (String): The development approach (e.g., `"programmatic"`).
-   `is_ai_tool` (Integer): A boolean flag (0/1) indicating if it is an AI-related node.
-   `is_trigger` (Integer): A boolean flag (0/1) indicating if it is a trigger node.
-   `is_webhook` (Integer): A boolean flag (0/1) indicating if it handles webhooks.
-   `is_versioned` (Integer): A boolean flag (0/1) indicating if the node supports versioning.
-   `version` (String): The current version number (e.g., `"2.1"`).
-   `documentation` (Text): Full markdown documentation content.
-   `properties_schema` (JSON/Text): The JSON schema defining node parameters and options.
-   `operations` (JSON/Text): Available operations or methods for the node.
-   `credentials_required` (JSON/Text): Required credential configurations.
-   `updated_at` (Timestamp): The timestamp of the last update.

## How to Import Your Full Dataset

To populate the database with your complete set of n8n nodes, follow these steps:

1.  **Clone the repository** to your local machine.
2.  **Replace the contents** of the `nodes/db.json` file with your complete JSON array of nodes.
3.  **Commit and push** the changes to your forked repository.

## API Access and Querying

You can access the node database using the following methods:

### 1. Raw File Access

This is the simplest method for retrieving the entire database. Use a raw file URL to fetch the JSON data directly.

**Endpoint:**
`https://raw.githubusercontent.com/{your-username}/{repository-name}/main/nodes/db.json`

**Example using `curl`:**

```bash
curl https://raw.githubusercontent.com/{your-username}/{repository-name}/main/nodes/db.json
```

### 2. GitHub API

The GitHub API provides more advanced querying capabilities, allowing you to retrieve specific information without downloading the entire file.

**Endpoint:**
`https://api.github.com/repos/{your-username}/{repository-name}/contents/nodes/db.json`

**Example using `curl`:**

```bash
curl -H "Accept: application/vnd.github.v3.raw" \
  https://api.github.com/repos/{your-username}/{repository-name}/contents/nodes/db.json
```

## Query Examples

Once you have fetched the JSON data, you can filter and search it within your n8n workflow or any other application. Here are some common query patterns using JavaScript:

### Find Nodes by Category

```javascript
const nodes = /* your fetched JSON data */;
const aiNodes = nodes.filter(node => node.category === 'ai');
console.log(aiNodes);
```

### Filter by Node Capabilities

```javascript
const nodes = /* your fetched JSON data */;
const triggerNodes = nodes.filter(node => node.is_trigger === 1);
const webhookNodes = nodes.filter(node => node.is_webhook === 1);
console.log(triggerNodes);
console.log(webhookNodes);
```

### Search by Display Name or Description

```javascript
const nodes = /* your fetched JSON data */;
const searchTerm = 'webhook';
const searchResults = nodes.filter(node =>
    node.display_name.toLowerCase().includes(searchTerm) ||
    node.description.toLowerCase().includes(searchTerm)
);
console.log(searchResults);
```

### Retrieve Full Documentation and Schemas

```javascript
const nodes = /* your fetched JSON data */;
const webhookNode = nodes.find(node => node.node_type === 'nodes-base.webhook');
console.log(webhookNode.documentation);
console.log(JSON.parse(webhookNode.properties_schema));
```

### Get Nodes by Package Name

```javascript
const nodes = /* your fetched JSON data */;
const langchainNodes = nodes.filter(node => node.package_name === 'n8n-nodes-langchain');
console.log(langchainNodes);
```

## Update Mechanism

To keep the database current, you can follow these steps:

1.  **Update Locally**: Modify the `nodes/db.json` file with any new or updated node information.
2.  **Commit Changes**: Commit the updated file to your local Git repository.
3.  **Push to GitHub**: Push the changes to the `main` branch to make them accessible via the API.

For automated updates, you could create a script that:
-   Fetches the latest node information from its source.
-   Formats the data into the required JSON structure.
-   Commits and pushes the updated `db.json` file to this repository.

This approach ensures your n8n automation always has access to the most recent node data.
