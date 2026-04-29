<div align="center">
  <h1> AWS AI Security Remediation Bot</h1>
  <p><i>An automated, zero-trust DevSecOps pipeline that auto-fixes infrastructure vulnerabilities.</i></p>
</div>

---

## 📖 Overview

This repository demonstrates a fully automated, passwordless DevSecOps pipeline. When insecure Terraform infrastructure is pushed to the repository, the pipeline detects the vulnerability, securely queries an enterprise AI model, and automatically writes the fix—opening a Pull Request without human intervention.

## 🏗️ Architecture & Tech Stack

| Component | Technology Used |
| :--- | :--- |
| **Cloud Provider** | AWS (Amazon Web Services) |
| **Infrastructure as Code** | Terraform |
| **CI/CD Automation** | GitHub Actions |
| **Security Scanner** | Checkov |
| **Authentication** | AWS IAM OIDC *(Passwordless)* |
| **Generative AI** | Amazon Bedrock *(Anthropic Claude Sonnet 4.6)* |
| **Scripting & Logic** | Python 3.12 (`boto3`, `PyGithub`) |

---

## ⚙️ How It Works

1. **The Trigger:** A developer pushes a misconfigured Terraform file (e.g., an S3 bucket with public access enabled) to the `main` branch.
2. **The Scan:** GitHub Actions spins up and runs `Checkov`. The scanner detects the security vulnerability and intentionally fails the step, preserving the error output.
3. **Secure Authentication:** The pipeline securely authenticates to AWS using **OpenID Connect (OIDC)**, assuming a temporary, least-privilege IAM role without utilizing any hardcoded access keys.
4. **AI Remediation:** A Python script packages the vulnerable code along with the Checkov alert context and securely sends it to Amazon Bedrock via the Converse API. 
5. **Automated PR:** Bedrock returns the securely rewritten Terraform code. The Python script then creates a new branch, commits the fix, and opens a Pull Request back to the `main` branch for human review.

---

## 🚀 Setup & Deployment Requirements

To replicate or run this pipeline in your own environment, you will need the following configuration:

> **Note:** This project utilizes the AWS Free Tier, but ensure you understand your cloud provider's pricing model before provisioning resources.

* [x] An AWS Account with access to **Amazon Bedrock** (Claude Sonnet 4.6).
* [x] An **AWS IAM OIDC Provider** configured to trust this specific GitHub repository.
* [x] An IAM Role (`GitHubActionsBedrockRole`) with `bedrock:InvokeModel` permissions.
* [x] A **GitHub Fine-Grained Personal Access Token (PAT)** with Read/Write access to `Contents`, `Pull Requests`, and `Workflows`, saved as a repository secret named `PAT_TOKEN`.

---
<div align="center">
  <i>Built with security, automation, and AI in mind.</i>
</div>
