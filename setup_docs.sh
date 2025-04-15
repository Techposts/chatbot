#!/bin/bash

# Create docs directory if it doesn't exist
mkdir -p /var/www/anaptyss-chatbot/docs

# Create or update services.md
cat > /var/www/anaptyss-chatbot/docs/services.md << 'EOL'
# Anaptyss Services

## Data Analytics Solutions

Anaptyss provides comprehensive data analytics solutions to help businesses extract actionable insights from their data. Our services include:

### Data Visualization

Transform complex data into intuitive visual representations that make it easy to identify patterns, trends, and outliers. Our data visualization services include:

- Interactive dashboards
- Custom charts and graphs
- Real-time data visualizations
- Executive reporting tools

### Predictive Analytics

Leverage advanced algorithms and machine learning to forecast future trends and behaviors. Our predictive analytics capabilities include:

- Sales forecasting
- Customer churn prediction
- Inventory optimization
- Risk assessment models

### Business Intelligence Dashboards

Consolidate data from multiple sources into unified, interactive dashboards that provide a 360-degree view of your business performance:

- KPI tracking dashboards
- Sales and marketing analytics
- Financial performance monitoring
- Operational efficiency metrics

## Implementation Approaches

We offer flexible implementation options to meet your specific needs:

1. **Custom Solutions**: Built from scratch to address your unique requirements
2. **Platform Integration**: Connect with your existing tools and platforms
3. **Managed Services**: Ongoing support and optimization of your analytics infrastructure

## Industries We Serve

- Retail and E-commerce
- Financial Services
- Healthcare
- Manufacturing
- Logistics and Supply Chain
- SaaS and Technology
EOL

# Create or update pricing.md
cat > /var/www/anaptyss-chatbot/docs/pricing.md << 'EOL'
# Anaptyss Pricing

At Anaptyss, we understand that every business has unique data analytics needs. Our pricing is designed to be flexible and scalable based on your specific requirements.

## Pricing Models

### Project-Based

For businesses with specific, well-defined analytics needs:

- **Starter**: $5,000-$15,000
  - Basic data visualization
  - Single-source data integration
  - Up to 3 custom dashboards

- **Professional**: $15,000-$30,000
  - Advanced visualizations
  - Multi-source data integration
  - Up to 10 custom dashboards
  - Basic predictive models

- **Enterprise**: $30,000+
  - Comprehensive analytics solution
  - Complex data integration
  - Unlimited dashboards
  - Advanced predictive models
  - Custom algorithms

### Subscription-Based

For ongoing analytics needs with regular updates and maintenance:

- **Basic**: $1,500/month
  - Up to 5 dashboards
  - Monthly data updates
  - Basic support

- **Standard**: $3,000/month
  - Up to 15 dashboards
  - Weekly data updates
  - Priority support
  - Quarterly review and optimization

- **Premium**: $5,000+/month
  - Unlimited dashboards
  - Real-time data updates
  - 24/7 premium support
  - Monthly review and optimization
  - Dedicated analyst

## Additional Services

- **Data Integration**: Starting at $2,500
- **Custom Algorithm Development**: Starting at $5,000
- **Training and Workshops**: $1,500 per session
- **Maintenance and Support**: Starting at $800/month

## Get a Custom Quote

Every business is unique, and so are your data analytics needs. Contact us for a personalized consultation and quote tailored to your specific requirements.

*All prices are in USD and subject to change based on project scope and complexity.*
EOL

# Create or update about.md
cat > /var/www/anaptyss-chatbot/docs/about.md << 'EOL'
# About Anaptyss

## Our Mission

At Anaptyss, our mission is to transform complex data into clear, actionable insights that empower businesses to make confident, data-driven decisions. We believe that every organization, regardless of size or industry, should have access to powerful analytics tools that unlock the full potential of their data.

## Our Story

Founded in 2021, Anaptyss emerged from the recognition that while businesses were collecting vast amounts of data, many struggled to effectively analyze and leverage this information for strategic advantage. Our founders, with backgrounds in data science, business intelligence, and enterprise software, came together with a shared vision: to bridge the gap between raw data and meaningful business insights.

Starting with a small team of data scientists and engineers, we developed our first custom analytics solutions for clients in the retail and financial sectors. The impact was immediate and significant, leading to rapid growth and expansion into new industries.

Today, Anaptyss serves clients across multiple industries, helping them harness the power of their data to drive innovation, optimize operations, and accelerate growth.

## Our Approach

We believe in a collaborative, client-centered approach to data analytics. Our process includes:

1. **Discovery**: Understanding your business, goals, and unique challenges
2. **Design**: Creating tailored analytics solutions that address your specific needs
3. **Development**: Building robust, scalable data pipelines and visualizations
4. **Deployment**: Implementing solutions seamlessly into your existing workflows
5. **Optimization**: Continuously refining and enhancing your analytics capabilities

## Our Team

Anaptyss brings together experts in:

- Data Science and Machine Learning
- Business Intelligence
- Software Engineering
- UX/UI Design
- Industry-Specific Domain Knowledge

Our diverse team combines technical excellence with business acumen to deliver solutions that not only analyze data effectively but also address real business challenges.

## Why Choose Anaptyss?

- **Customized Solutions**: Tailored to your specific business needs
- **Industry Expertise**: Deep understanding of sector-specific challenges
- **Cutting-Edge Technology**: Leveraging the latest advancements in data science
- **Scalable Approach**: Solutions that grow with your business
- **Proven Results**: Track record of delivering measurable business impact

## Get in Touch

We're excited to learn about your business and explore how our data analytics solutions can help you achieve your goals. Contact us today to start the conversation.
EOL

# Create or update model_risk.md
cat > /var/www/anaptyss-chatbot/docs/model_risk.md << 'EOL'
# Model Risk Management

## Overview

Anaptyss provides comprehensive Model Risk Management (MRM) solutions designed to help financial institutions and businesses effectively identify, measure, monitor, and mitigate risks associated with their analytical and decision-making models. Our MRM services ensure regulatory compliance while optimizing model performance and reliability.

## Key Services

### Model Validation and Verification

We provide independent validation and verification of your analytical models to ensure they are conceptually sound, statistically robust, and fit-for-purpose:

- Comprehensive model documentation review
- Methodology and assumptions assessment
- Code review and implementation verification
- Performance testing and back-testing
- Sensitivity analysis and stress testing
- Benchmark comparison against alternative models

### Risk Assessment Frameworks

We help organizations develop and implement robust model risk assessment frameworks:

- Model risk tiering and classification
- Quantitative risk scoring methodologies
- Risk appetite definition and monitoring
- Customized risk matrices for different model types
- Automated risk assessment tools

### Regulatory Compliance Support

Our solutions are designed to ensure compliance with relevant regulatory requirements:

- SR 11-7 (Federal Reserve) compliance
- OCC 2011-12 guidance alignment
- FRTB (Fundamental Review of the Trading Book) requirements
- CECL (Current Expected Credit Loss) model validation
- IFRS 9 compliance support
- AI/ML model governance for emerging regulations

### Model Governance Systems

We help establish comprehensive model governance structures:

- Model inventory management systems
- Model lifecycle management
- Role and responsibility frameworks
- Model change control processes
- Ongoing monitoring and periodic review protocols
- Executive and board reporting mechanisms

## Implementation Approach

Our approach to implementing Model Risk Management solutions follows these key phases:

1. **Assessment**: Evaluating current model landscape and governance structure
2. **Design**: Developing tailored MRM frameworks and processes
3. **Implementation**: Deploying solutions with appropriate documentation and training
4. **Monitoring**: Establishing continuous oversight mechanisms
5. **Optimization**: Refining processes based on operational feedback and evolving requirements

## Benefits of Anaptyss MRM Solutions

- **Regulatory Compliance**: Meet supervisory expectations and avoid regulatory issues
- **Enhanced Decision Making**: Improve confidence in model outputs and business decisions
- **Operational Efficiency**: Streamline validation processes and reduce manual efforts
- **Risk Mitigation**: Proactively identify and address potential model weaknesses
- **Competitive Advantage**: Leverage more sophisticated models with proper controls

## Client Success Stories

Our MRM solutions have helped clients achieve significant improvements in model risk management:

- Reduced model validation time by 40% for a mid-sized bank
- Identified critical flaws in credit risk models, preventing potential losses of over $2M
- Streamlined model governance processes, resulting in successful regulatory examinations
- Enabled safe deployment of advanced AI/ML models with appropriate controls and monitoring

## Industries Served

While our MRM solutions are particularly relevant for financial services, we also support:

- Insurance companies
- Healthcare organizations
- Energy and utilities
- Manufacturing with complex optimization models
- Retail and e-commerce businesses using predictive models
EOL

# Set permissions
chmod 644 /var/www/anaptyss-chatbot/docs/*.md

# Install MCP filesystem server if not already installed
if ! command -v npx &> /dev/null
then
    echo "Installing Node.js and npm..."
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi

# Install the MCP filesystem server
npm install -g @modelcontextprotocol/server-filesystem

# Restart the chatbot service
sudo systemctl restart anaptyss-chatbot

echo "Documentation setup complete. Chatbot service restarted."
