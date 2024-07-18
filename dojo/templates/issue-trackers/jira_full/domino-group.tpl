{% load navigation_tags %}
{% load display_tags %}
{% url 'view_finding_group' finding_group.id as finding_group_url %}
{% url 'view_product' finding.test.engagement.product.id as product_url %}
{% url 'view_engagement' finding.test.engagement.id as engagement_url %}
{% url 'view_test' finding.test.id as test_url %}

A group of Findings has been pushed to JIRA to be investigated and fixed:

h2. Group
*Group*: [{{ finding_group.name|jiraencode}}|{{ finding_group_url|full_url }}] in [{{ finding_group.test.engagement.product.name|jiraencode }}|{{ product_url|full_url }}] / [{{ finding_group.test.engagement.name|jiraencode }}|{{ engagement_url|full_url }}] / [{{ finding_group.test|stringformat:'s'|jiraencode }}|{{ test_url|full_url }}]

h2. Wiki on fix expectations and validation

https://dominodatalab.atlassian.net/wiki/spaces/ISAC/pages/2243461464/Vulnerability+management+expectations

Data Imported on : {{finding_group.test.updated}}

|| ID || Severity || CVE || Component || Version || Status || Fixed In ||| File Path ||| Date First Found || Vuln Type || Tool ||{% for finding in finding_group.findings.all %}
| {{finding.id}} | {{finding.severity}} | {% if finding.cve %}[{{finding.cve}}|{{finding.cve|vulnerability_url}}]{% else %}None{% endif %} | {{finding.component_name|jiraencode_component}} | {{finding.component_version}} | {{ finding.status }} | {% if finding.mitigation %}{{ finding.mitigation }}{% else %}None{% endif %} | {{finding.file_path}} | {{finding.created}} | {{finding.vuln_id_from_tool}} | {{finding.unique_id_from_tool}} |{% endfor %}
