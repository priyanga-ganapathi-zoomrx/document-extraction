"""
Pharmaceutical database schema definition.
This file contains the complete schema structure used for data extraction and mapping.
"""

PHARMA_SCHEMA = {
    "core_entities": {
        "companies": {
            "description": "Information about pharmaceutical companies and organizations",
            "fields": {
                "name": "Official company name",
                "type": "Company type (e.g., Pharma, Biotech)",
                "stock_symbol": "Stock market symbol",
                "hq_location": "Headquarters location"
            }
        },
        "drugs": {
            "description": "Information about pharmaceutical compounds and therapies",
            "fields": {
                "name": "Drug name or identifier",
                "mechanism": "Mechanism of action",
                "development_stage": "Current development stage (e.g., Phase I, Approved)",
                "approval_status": "Regulatory approval status"
            }
        },
        "diseases": {
            "description": "Information about diseases and conditions",
            "fields": {
                "name": "Disease name",
                "disease_type": "Category or type of disease",
                "parent_disease_id": "Reference to parent disease if this is a subtype"
            }
        },
        "molecular_targets": {
            "description": "Information about molecular targets for drugs",
            "fields": {
                "name": "Target name",
                "target_type": "Type of target (e.g., receptor, enzyme)",
                "gene_symbol": "Gene symbol if applicable",
                "uniprot_id": "UniProt identifier if applicable"
            }
        },
        "therapeutic_modalities": {
            "description": "Types of therapeutic approaches",
            "fields": {
                "name": "Modality name",
                "description": "Description of the modality",
                "modality_level": "Classification level of modality"
            }
        },
        "geographies": {
            "description": "Information about geographic regions",
            "fields": {
                "name": "Geographic name",
                "code": "Region code",
                "geography_type": "Type of geography (e.g., country, region)"
            }
        },
        "drug_classes": {
            "description": "Classification of drugs by therapeutic class",
            "fields": {
                "name": "Class name",
                "description": "Description of the drug class",
                "parent_class_id": "Reference to parent class if this is a subclass"
            }
        }
    },
    "document_references": {
        "document_sources": {
            "description": "Information about source documents",
            "fields": {
                "document_title": "Title of the document",
                "document_type": "Type of document (e.g., presentation, publication)",
                "company_id": "Reference to the company associated with the document",
                "document_date": "Date the document was published or presented"
            }
        },
        "document_locations": {
            "description": "Specific locations within documents",
            "fields": {
                "document_id": "Reference to the document",
                "location_type": "Type of location (e.g., page, slide, section)",
                "page_number": "Page or slide number",
                "section_name": "Name of the section within the document"
            }
        },
        "entity_source_references": {
            "description": "References linking entities to their document sources",
            "fields": {
                "entity_type": "Type of entity being referenced",
                "entity_id": "Reference to the entity",
                "document_location_id": "Reference to the document location"
            }
        },
        "field_citations": {
            "description": "Citations for specific data fields",
            "fields": {
                "entity_type": "Type of entity containing the field",
                "entity_id": "Reference to the entity",
                "field_name": "Name of the cited field",
                "document_location_id": "Reference to the document location"
            }
        },
        "entity_synonyms": {
            "description": "Alternative names or synonyms for entities",
            "fields": {
                "entity_type": "Type of entity",
                "canonical_form": "Standard form of the entity name",
                "synonym": "Alternative name or abbreviation",
                "synonym_type": "Type of synonym (e.g., abbreviation, brand name)"
            }
        }
    },
    "indication_specifications": {
        "indication_specifications": {
            "description": "Detailed specifications for disease indications",
            "fields": {
                "disease_id": "Reference to the disease",
                "biomarker_status": "Relevant biomarker status",
                "line_of_therapy": "Line of therapy (e.g., first-line, second-line)",
                "disease_stage": "Stage of disease"
            }
        },
        "combination_indication_specifications": {
            "description": "Specifications for combination therapy indications",
            "fields": {
                "combination_id": "Reference to the drug combination",
                "disease_id": "Reference to the disease",
                "biomarker_status": "Relevant biomarker status"
            }
        }
    },
    "relationships": {
        "entity_relationships": {
            "description": "Relationships between different entities",
            "fields": {
                "source_entity_type": "Type of source entity",
                "source_entity_id": "Reference to source entity",
                "relationship_type": "Type of relationship",
                "target_entity_type": "Type of target entity",
                "target_entity_id": "Reference to target entity"
            }
        },
        "relationship_type_reference": {
            "description": "Reference information about relationship types",
            "fields": {
                "relationship_category": "Category of relationship",
                "relationship_type": "Type of relationship",
                "description": "Description of the relationship"
            }
        },
        "drug_trial_details": {
            "description": "Details of drugs in clinical trials",
            "fields": {
                "relationship_id": "Reference to the relationship",
                "dosage": "Dosage information",
                "treatment_duration": "Duration of treatment",
                "outcome_summary": "Summary of outcomes"
            }
        }
    },
    "drug_development": {
        "research_programs": {
            "description": "Research and development programs",
            "fields": {
                "company_id": "Reference to the company",
                "program_name": "Name of the research program",
                "therapeutic_area": "Therapeutic area of focus",
                "stage": "Current development stage"
            }
        },
        "drug_targets": {
            "description": "Targets of drugs",
            "fields": {
                "drug_id": "Reference to the drug",
                "target_id": "Reference to the molecular target",
                "relationship_type": "Type of drug-target relationship",
                "binding_affinity": "Binding affinity information"
            }
        },
        "drug_modalities": {
            "description": "Therapeutic modalities of drugs",
            "fields": {
                "drug_id": "Reference to the drug",
                "modality_id": "Reference to the therapeutic modality",
                "is_primary": "Indicator if this is the primary modality"
            }
        },
        "drug_combinations": {
            "description": "Combination therapies",
            "fields": {
                "combination_name": "Name of the combination",
                "combination_type": "Type of combination",
                "rationale": "Rationale for the combination"
            }
        },
        "drug_development_roles": {
            "description": "Roles of companies in drug development",
            "fields": {
                "drug_id": "Reference to the drug",
                "company_id": "Reference to the company",
                "development_role": "Role in development (e.g., originator, licensee)",
                "geography_id": "Reference to geographic scope"
            }
        },
        "drug_combination_components": {
            "description": "Components of drug combinations",
            "fields": {
                "combination_id": "Reference to the combination",
                "drug_id": "Reference to the drug component",
                "role_in_combination": "Role of this drug in the combination"
            }
        }
    },
    "clinical": {
        "clinical_trials": {
            "description": "Clinical trials for pharmaceutical products",
            "fields": {
                "nct_id": "ClinicalTrials.gov identifier",
                "title": "Title of the clinical trial",
                "status": "Trial status (e.g., recruiting, completed)",
                "phase": "Clinical trial phase",
                "enrollment": "Number of participants enrolled"
            }
        },
        "clinical_trial_design": {
            "description": "Design details of clinical trials",
            "fields": {
                "trial_id": "Reference to the clinical trial",
                "design_type": "Type of trial design (e.g., randomized, open-label)",
                "blinding": "Blinding approach used",
                "randomization_ratio": "Ratio for randomization"
            }
        },
        "clinical_trial_arms": {
            "description": "Arms or treatment groups in clinical trials",
            "fields": {
                "trial_id": "Reference to the clinical trial",
                "arm_name": "Name of the trial arm",
                "arm_type": "Type of arm (e.g., experimental, control)",
                "is_control": "Indicator if this is a control arm"
            }
        },
        "clinical_trial_sites": {
            "description": "Sites conducting clinical trials",
            "fields": {
                "trial_id": "Reference to the clinical trial",
                "site_name": "Name of the trial site",
                "institution_name": "Name of the institution",
                "location": "Geographic location of the site"
            }
        },
        "clinical_trial_indications": {
            "description": "Indications being studied in clinical trials",
            "fields": {
                "trial_id": "Reference to the clinical trial",
                "disease_id": "Reference to the disease",
                "indication_specification_id": "Reference to specific indication"
            }
        },
        "trial_enrollment_tracking": {
            "description": "Tracking of patient enrollment in trials",
            "fields": {
                "trial_id": "Reference to the clinical trial",
                "report_date": "Date of enrollment report",
                "cumulative_enrollment": "Cumulative number of patients enrolled"
            }
        },
        "clinical_data_points": {
            "description": "Data points from clinical trials",
            "fields": {
                "trial_id": "Reference to the clinical trial",
                "endpoint_type": "Type of endpoint",
                "endpoint_name": "Name of the endpoint",
                "value": "Value of the data point"
            }
        }
    },
    "regulatory": {
        "regulatory_authorities": {
            "description": "Regulatory agencies and authorities",
            "fields": {
                "name": "Name of regulatory authority",
                "shortcode": "Abbreviation or code for the authority",
                "geography_id": "Reference to geographic jurisdiction"
            }
        },
        "regulatory_submissions": {
            "description": "Submissions to regulatory authorities",
            "fields": {
                "drug_id": "Reference to the drug",
                "geography_id": "Reference to the geography",
                "submission_date": "Date of submission",
                "submission_type": "Type of submission (e.g., NDA, MAA)"
            }
        },
        "regulatory_approvals": {
            "description": "Regulatory approvals for drugs",
            "fields": {
                "drug_id": "Reference to the drug",
                "indication_specification_id": "Reference to the specific indication",
                "approval_date": "Date of regulatory approval"
            }
        },
        "regulatory_designations": {
            "description": "Special regulatory designations for drugs",
            "fields": {
                "drug_id": "Reference to the drug",
                "designation_type": "Type of designation (e.g., Orphan Drug, Fast Track)",
                "status": "Status of the designation",
                "designation_date": "Date the designation was granted"
            }
        },
        "patents": {
            "description": "Patent information for drugs",
            "fields": {
                "patent_number": "Patent number",
                "title": "Patent title",
                "filing_date": "Date the patent was filed",
                "expiration_date": "Date the patent expires"
            }
        },
        "regulatory_exclusivity": {
            "description": "Exclusivity periods for drugs",
            "fields": {
                "drug_id": "Reference to the drug",
                "exclusivity_type": "Type of exclusivity",
                "start_date": "Start date of exclusivity",
                "end_date": "End date of exclusivity"
            }
        },
        "regulatory_communications": {
            "description": "Communications with regulatory authorities",
            "fields": {
                "drug_id": "Reference to the drug",
                "authority_id": "Reference to the regulatory authority",
                "communication_date": "Date of communication",
                "communication_type": "Type of communication"
            }
        }
    },
    "treatment": {
        "regimens": {
            "description": "Treatment regimens",
            "fields": {
                "name": "Name of the regimen",
                "primary_indication": "Primary indication for the regimen",
                "regimen_type": "Type of regimen",
                "guideline_reference": "Reference to clinical guidelines"
            }
        },
        "regimen_components": {
            "description": "Components of treatment regimens",
            "fields": {
                "regimen_id": "Reference to the regimen",
                "component_type": "Type of component",
                "drug_id": "Reference to the drug",
                "administration_timing": "Timing of administration"
            }
        },
        "regimen_efficacy_comparisons": {
            "description": "Efficacy comparisons between regimens",
            "fields": {
                "primary_regimen_id": "Reference to the primary regimen",
                "comparator_regimen_id": "Reference to the comparator regimen",
                "disease_id": "Reference to the disease"
            }
        },
        "regimen_safety_comparisons": {
            "description": "Safety comparisons between regimens",
            "fields": {
                "primary_regimen_id": "Reference to the primary regimen",
                "comparator_regimen_id": "Reference to the comparator regimen",
                "safety_parameter": "Parameter being compared"
            }
        },
        "standard_of_care": {
            "description": "Standard of care treatments",
            "fields": {
                "disease_id": "Reference to the disease",
                "geography_id": "Reference to the geography",
                "regimen_id": "Reference to the regimen",
                "line_of_therapy": "Line of therapy"
            }
        }
    },
    "commercial": {
        "drug_brands": {
            "description": "Brand names for drugs",
            "fields": {
                "drug_id": "Reference to the drug",
                "brand_name": "Brand name",
                "company_id": "Reference to the company",
                "geography_id": "Reference to the geography"
            }
        },
        "drug_pricing": {
            "description": "Pricing information for drugs",
            "fields": {
                "drug_id": "Reference to the drug",
                "geography_id": "Reference to the geography",
                "price_type": "Type of price (e.g., list, net)",
                "price_value": "Price value",
                "effective_date": "Date the price became effective"
            }
        },
        "market_sizing": {
            "description": "Market size information",
            "fields": {
                "disease_id": "Reference to the disease",
                "geography_id": "Reference to the geography",
                "year": "Year of the market size estimate",
                "patient_count": "Number of patients",
                "revenue_value": "Revenue value"
            }
        },
        "drug_market_forecasts": {
            "description": "Market forecasts for drugs",
            "fields": {
                "drug_id": "Reference to the drug",
                "disease_id": "Reference to the disease",
                "geography_id": "Reference to the geography",
                "year": "Year of the forecast",
                "revenue_forecast": "Forecasted revenue"
            }
        },
        "competitive_landscape": {
            "description": "Competitive landscape information",
            "fields": {
                "disease_id": "Reference to the disease",
                "geography_id": "Reference to the geography",
                "year": "Year of the assessment",
                "market_leader_id": "Reference to the market leader"
            }
        },
        "market_access_status": {
            "description": "Market access status for drugs",
            "fields": {
                "drug_id": "Reference to the drug",
                "geography_id": "Reference to the geography",
                "launch_date": "Date of market launch",
                "access_level": "Level of market access"
            }
        },
        "market_catalysts": {
            "description": "Market catalysts or events",
            "fields": {
                "disease_id": "Reference to the disease",
                "drug_id": "Reference to the drug",
                "catalyst_date": "Date of the catalyst",
                "catalyst_type": "Type of catalyst",
                "description": "Description of the catalyst"
            }
        }
    },
    "financial": {
        "business_deals": {
            "description": "Business deals and transactions",
            "fields": {
                "deal_name": "Name of the deal",
                "deal_type": "Type of deal (e.g., acquisition, licensing)",
                "status": "Status of the deal",
                "announcement_date": "Date the deal was announced",
                "upfront_payment": "Upfront payment amount"
            }
        },
        "partnership_details": {
            "description": "Details of partnerships",
            "fields": {
                "deal_id": "Reference to the deal",
                "geographic_scope": "Geographic scope of the partnership",
                "therapeutic_areas": "Therapeutic areas covered",
                "exclusivity_terms": "Terms of exclusivity"
            }
        },
        "investments": {
            "description": "Investment information",
            "fields": {
                "company_id": "Reference to the company",
                "investor_id": "Reference to the investor",
                "investment_type": "Type of investment",
                "amount": "Investment amount",
                "investment_date": "Date of investment"
            }
        },
        "transaction_parties": {
            "description": "Parties involved in transactions",
            "fields": {
                "deal_id": "Reference to the deal",
                "company_id": "Reference to the company",
                "party_role": "Role in the transaction",
                "investment_amount": "Amount invested or received"
            }
        },
        "licensing_details": {
            "description": "Details of licensing agreements",
            "fields": {
                "deal_id": "Reference to the deal",
                "license_type": "Type of license",
                "field_of_use": "Field of use for the license",
                "territory_scope": "Geographic scope of the license"
            }
        },
        "investment_rounds": {
            "description": "Investment funding rounds",
            "fields": {
                "company_id": "Reference to the company",
                "round_name": "Name of the investment round",
                "closing_date": "Date the round closed",
                "total_raised": "Total amount raised"
            }
        }
    },
    "research_evidence": {
        "scientific_publications": {
            "description": "Scientific publications",
            "fields": {
                "publication_type": "Type of publication",
                "title": "Publication title",
                "authors": "Publication authors",
                "journal_name": "Name of the journal",
                "publication_date": "Date of publication"
            }
        },
        "scientific_events": {
            "description": "Scientific events and conferences",
            "fields": {
                "name": "Name of the event",
                "event_type": "Type of event",
                "start_date": "Start date of the event",
                "end_date": "End date of the event",
                "location": "Location of the event"
            }
        },
        "scientific_presentations": {
            "description": "Presentations at scientific events",
            "fields": {
                "entity_publication_id": "Reference to the publication",
                "presentation_date": "Date of presentation",
                "presentation_type": "Type of presentation"
            }
        },
        "publication_results": {
            "description": "Results reported in publications",
            "fields": {
                "publication_id": "Reference to the publication",
                "result_type": "Type of result",
                "endpoint_name": "Name of the endpoint",
                "result_value": "Value of the result"
            }
        },
        "people": {
            "description": "People in the pharmaceutical field",
            "fields": {
                "name": "Person's name",
                "therapeutic_focus": "Therapeutic area of focus",
                "functional_expertise": "Functional expertise",
                "background": "Professional background"
            }
        },
        "employment": {
            "description": "Employment information",
            "fields": {
                "person_id": "Reference to the person",
                "company_id": "Reference to the company",
                "title": "Job title",
                "department": "Department",
                "role_type": "Type of role"
            }
        }
    },
    "lifecycle_events": {
        "entity_milestones": {
            "description": "Milestones for entities",
            "fields": {
                "entity_type": "Type of entity",
                "entity_id": "Reference to the entity",
                "milestone_category": "Category of milestone",
                "milestone_name": "Name of the milestone",
                "planned_date": "Planned date for the milestone"
            }
        },
        "program_terminations": {
            "description": "Terminations of research programs",
            "fields": {
                "termination_date": "Date of termination",
                "program_id": "Reference to the program",
                "drug_id": "Reference to the drug",
                "termination_type": "Type of termination"
            }
        },
        "termination_data_points": {
            "description": "Data points related to terminations",
            "fields": {
                "termination_id": "Reference to the termination",
                "data_type": "Type of data",
                "metric_name": "Name of the metric",
                "observed_value": "Observed value"
            }
        },
        "milestone_types": {
            "description": "Types of milestones",
            "fields": {
                "milestone_category": "Category of milestone",
                "milestone_type": "Type of milestone",
                "significance_level": "Level of significance"
            }
        }
    },
    "metadata": {
        "entity_versions": {
            "description": "Version information for entities",
            "fields": {
                "entity_type": "Type of entity",
                "entity_id": "Reference to the entity",
                "version_number": "Version number",
                "change_timestamp": "Timestamp of the change"
            }
        },
        "data_source_metadata": {
            "description": "Metadata about data sources",
            "fields": {
                "source_name": "Name of the source",
                "source_type": "Type of source",
                "quality_assessment": "Assessment of data quality"
            }
        },
        "entity_resolution_log": {
            "description": "Log of entity resolution actions",
            "fields": {
                "entity_type": "Type of entity",
                "entity_id": "Reference to the entity",
                "resolution_action": "Type of resolution action",
                "confidence": "Confidence in the resolution"
            }
        },
        "schema_evolution": {
            "description": "Information about schema changes",
            "fields": {
                "entity_type": "Type of entity",
                "json_path": "JSON path to the schema element",
                "description": "Description of the schema element",
                "value_type": "Data type of the value"
            }
        }
    }
}

    