# Stuart Allan — Certified Cloud Practitioner Portfolio

A personal portfolio website hosted on AWS, showcasing my cloud certifications, projects, work history and skills. Live at [www.stuart-allan.com](https://www.stuart-allan.com).

---

## Features

- **Hero section** — name, title and professional tagline
- **About Me** — professional background and career summary
- **Technical Skills** — AWS core services, cloud security, networking, cost optimisation and monitoring
- **Credentials & Resources** — links to AWS Skill Builder profile, AWS CCP certificate and CV
- **Projects** — cards linking to live projects
- **Contact Form** — serverless form submission via API Gateway → Lambda → SNS
- **Live Visitor Counter** — real-time count powered by DynamoDB and Lambda
- **CV page** — full work history, education, certifications and project portfolio

---

## Architecture

```
Browser
  │
  ├── Static assets (HTML/CSS/JS)
  │     └── Amazon S3  ──►  Amazon CloudFront  ──►  Route 53 (www.stuart-allan.com)
  │
  ├── Visitor counter & contact form
  │     └── Amazon API Gateway  ──►  AWS Lambda  ──►  Amazon DynamoDB
  │                                               └──►  Amazon SNS  ──►  Email
```

### AWS Services Used

| Service | Purpose |
|---|---|
| Amazon S3 | Static website hosting |
| Amazon CloudFront | Global CDN and HTTPS delivery |
| Amazon Route 53 | Custom domain DNS |
| Amazon API Gateway | REST API front door for Lambda |
| AWS Lambda | Contact form processing and visitor counter |
| Amazon DynamoDB | Visitor count storage |
| Amazon SNS | Email notifications from the contact form |
| AWS IAM | Least-privilege permissions for all services |

---

## CI/CD

Every push to `main` triggers a GitHub Actions workflow that:

1. Syncs all static files to the S3 bucket
2. Invalidates the CloudFront cache so changes go live immediately

---

## Project Structure

```
.
├── index.html                  # Main portfolio page
├── cv.html                     # CV / résumé page
├── .github/
│   └── workflows/
│       └── deploy.yaml         # GitHub Actions CI/CD pipeline
```

---

## Local Development

No build step required — this is plain HTML, CSS and JavaScript. Open `index.html` directly in a browser to preview the portfolio layout.

Note: the visitor counter and contact form require the API Gateway endpoint to be reachable, so those features will not function locally without the AWS backend running.

---

## Author

**Stuart Allan**
- Portfolio: [www.stuart-allan.com](https://www.stuart-allan.com)
- LinkedIn: [linkedin.com/in/stuart-allan-595637409](https://www.linkedin.com/in/stuart-allan-595637409/)
- GitHub: [github.com/stuartallan1981](https://github.com/stuartallan1981)
