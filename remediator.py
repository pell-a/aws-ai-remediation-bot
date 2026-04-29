import boto3
from github import Github
import os

# 1. Setup Clients (AWS auth is handled automatically by the OIDC environment)
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
g = Github(os.environ["PAT_TOKEN"])
repo = g.get_repo(os.environ["GITHUB_REPOSITORY"])

# 2. Read the Vulnerable Code
file_path = "main.tf"
with open(file_path, "r") as file:
    bad_code = file.read()

vulnerability_details = "Checkov flagged CKV_AWS_20: S3 bucket has an ACL defined which allows public access."

# 3. Prompt Amazon Bedrock (Claude Sonnet 4.6)
prompt = f"""
You are an AWS DevSecOps expert. Fix the following Terraform vulnerability: {vulnerability_details}
Here is the code:
{bad_code}

Rewrite the `aws_s3_bucket_public_access_block` resource to enforce strict private access (set all blocks to true).
Return ONLY the raw Terraform code. Do not include markdown formatting like ```hcl or ```terraform.
"""

# Modern 2026 Converse API Method
response = bedrock.converse(
    modelId="anthropic.claude-sonnet-4-6",
    messages=[{"role": "user", "content": [{"text": prompt}]}],
    inferenceConfig={"maxTokens": 1000}
)

fixed_code = response['output']['message']['content'][0]['text']

# 4. Push to GitHub and Open a PR
branch_name = "security-fix-s3-bucket"
main_branch = repo.get_branch("main")
repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=main_branch.commit.sha)

contents = repo.get_contents(file_path, ref=branch_name)
repo.update_file(contents.path, "Automated Security Fix", fixed_code, contents.sha, branch=branch_name)

repo.create_pull(
    title="[SECURITY] Automated Infrastructure Fix", 
    body="Amazon Bedrock (Claude Sonnet 4.6) generated this fix to secure a public S3 bucket.", 
    head=branch_name, 
    base="main"
)

print("Modern Pull Request created successfully!")