PHARMA_SCHEMA = {
  "Core_Entity_Module": {
    "geographies": {
      "fields": [
        "id",
        "code",
        "name",
        "geography_type",
        "parent_geography_id",
        "data"
      ],
      "description": "Geographic regions, countries, states, and other locations"
    },
    "companies": {
      "fields": [
        "id",
        "name",
        "canonical_name",
        "company_type",
        "is_public",
        "stock_symbol",
        "parent_company_id",
        "hq_address",
        "hq_city",
        "hq_state",
        "hq_postal_code",
        "hq_country",
        "hq_metro_area",
        "hq_latitude",
        "hq_longitude",
        "last_update_date",
        "data",
        "source_type",
        "primary_source_id"
      ],
      "description": "Pharmaceutical and biotech companies"
    },
    "therapeutic_modalities": {
      "fields": [
        "id",
        "name",
        "canonical_name",
        "description",
        "modality_level",
        "parent_modality_id",
        "properties",
        "last_update_date",
        "data",
        "primary_source_id"
      ],
      "description": "Therapeutic approaches and modalities"
    },
    "diseases": {
      "fields": [
        "id",
        "name",
        "canonical_name",
        "disease_type",
        "parent_disease_id",
        "last_update_date",
        "data",
        "source_type",
        "primary_source_id"
      ],
      "description": "Disease and condition classifications"
    },
    "molecular_targets": {
      "fields": [
        "id",
        "name",
        "canonical_name",
        "target_type",
        "gene_symbol",
        "uniprot_id",
        "parent_target_id",
        "last_update_date",
        "data",
        "source_type",
        "primary_source_id"
      ],
      "description": "Molecular targets for drug development"
    },
    "drug_classes": {
      "fields": [
        "id",
        "name",
        "canonical_name",
        "description",
        "parent_class_id",
        "last_update_date",
        "data",
        "source_type",
        "primary_source_id"
      ],
      "description": "Classification system for drugs"
    },
    "drugs": {
      "fields": [
        "id",
        "name",
        "canonical_name",
        "mechanism",
        "development_stage",
        "is_disclosed",
        "first_approval_date",
        "first_approval_geography_id",
        "primary_company_id",
        "primary_modality_id",
        "last_update_date",
        "data",
        "source_type",
        "primary_source_id",
        "termination_id",
        "termination_date"
      ],
      "description": "Drug compounds and therapies"
    }
  },

  "Document_Reference_Module": {
    "document_sources": {
      "fields": [
        "id",
        "document_title",
        "document_type",
        "company_id",
        "document_date",
        "document_url",
        "file_path",
        "file_hash",
        "total_pages",
        "metadata",
        "ingestion_date",
        "last_update_date"
      ],
      "description": "Source documents for data extraction"
    },
    "document_locations": {
      "fields": [
        "id",
        "document_id",
        "location_type",
        "location_identifier",
        "page_number",
        "section_name",
        "content_snippet",
        "screenshot_path",
        "location_hash"
      ],
      "description": "Specific locations within documents"
    },
    "entity_source_references": {
      "fields": [
        "id",
        "entity_type",
        "entity_id",
        "document_location_id",
        "reference_type",
        "extracted_data",
        "confidence_score",
        "extraction_method",
        "extraction_date",
        "notes"
      ],
      "description": "References from entities to source documents"
    },
    "entity_synonyms": {
      "fields": [
        "id",
        "entity_type",
        "canonical_form",
        "synonym",
        "synonym_type",
        "confidence",
        "last_update_date",
        "primary_source_id"
      ],
      "description": "Alternative names for entities"
    },
    "field_citations": {
      "fields": [
        "id",
        "entity_type",
        "entity_id",
        "field_name",
        "document_location_id",
        "extraction_confidence",
        "extraction_date",
        "is_primary_source",
        "notes"
      ],
      "description": "Field-level citation tracking with primary source indicator"
    }
  },
  "Indication_Specifications_Module": {
    "indication_specifications": {
      "fields": [
        "id",
        "disease_id",
        "specification_text",
        "specification_summary",
        "biomarker_status",
        "line_of_therapy",
        "disease_stage",
        "prior_therapy_requirements",
        "combination_setting",
        "last_update_date",
        "data",
        "source_type",
        "primary_source_id"
      ],
      "description": "Disease contexts and treatment populations"
    },
    "combination_indication_specifications": {
      "fields": [
        "id",
        "combination_id",
        "disease_id",
        "specification_text",
        "specification_summary",
        "biomarker_status",
        "line_of_therapy",
        "disease_stage",
        "prior_therapy_requirements",
        "combination_rationale",
        "synergy_evidence",
        "last_update_date",
        "data",
        "source_type",
        "primary_source_id"
      ],
      "description": "Specifications for combination therapies"
    }
  },
  "Relationship_Module": {
    "entity_relationships": {
      "fields": [
        "id",
        "source_entity_type",
        "source_entity_id",
        "relationship_type",
        "target_entity_type",
        "target_entity_id",
        "confidence",
        "relationship_data",
        "last_update_date",
        "source_type",
        "primary_source_id"
      ],
      "description": "Relationships between entities"
    },
    "relationship_type_reference": {
      "fields": [
        "id",
        "relationship_category",
        "relationship_type",
        "description",
        "applicable_entity_types",
        "is_active"
      ],
      "description": "Reference table for relationship types"
    },
    "drug_trial_details": {
      "fields": [
        "id",
        "relationship_id",
        "dosage",
        "treatment_duration",
        "treatment_schedule",
        "arm_details",
        "outcome_summary",
        "biomarker_data",
        "last_update_date",
        "data",
        "primary_source_id"
      ],
      "description": "Detailed information about drugs in trials"
    }
  },
  "Drug_Development_Module": {
    "research_programs": {
      "fields": [
        "id",
        "company_id",
        "program_name",
        "therapeutic_area",
        "primary_modality_id",
        "stage",
        "disclosed_date",
        "last_update_date",
        "data",
        "source_type",
        "primary_source_id",
        "termination_id",
        "termination_date"
      ],
      "description": "Drug and therapy research programs"
    },
    "research_program_indications": {
      "fields": [
        "id",
        "program_id",
        "disease_id",
        "indication_type",
        "inclusion_date",
        "status",
        "indication_rationale",
        "biomarker_criteria",
        "priority_level",
        "data",
        "primary_source_id",
        "last_update_date"
      ],
      "description": "Disease indications for research programs"
    },
    "research_program_modalities": {
      "fields": [
        "id",
        "program_id",
        "modality_id",
        "is_primary",
        "is_platform_focus",
        "notes",
        "last_update_date",
        "primary_source_id"
      ],
      "description": "Therapeutic modalities used in research programs"
    },
    "drug_targets": {
      "fields": [
        "id",
        "drug_id",
        "combination_id",
        "target_id",
        "relationship_type",
        "binding_affinity",
        "affinity_value",
        "affinity_unit",
        "affinity_type",
        "is_primary",
        "target_engagement_evidence",
        "clinical_relevance",
        "confidence_level",
        "data",
        "primary_source_id",
        "last_update_date"
      ],
      "description": "Molecular targets of drugs"
    },
    "drug_modalities": {
      "fields": [
        "id",
        "drug_id",
        "combination_id",
        "modality_id",
        "is_primary",
        "notes",
        "last_update_date",
        "data",
        "primary_source_id"
      ],
      "description": "Therapeutic modalities of drugs"
    },
    "drug_development_roles": {
      "fields": [
        "id",
        "drug_id",
        "combination_id",
        "regimen_id",
        "company_id",
        "development_role",
        "development_phase",
        "geography_id",
        "start_date",
        "end_date",
        "is_current",
        "cost_sharing_arrangement",
        "deal_id",
        "data",
        "primary_source_id",
        "last_update_date"
      ],
      "description": "Company roles in drug development"
    },
    "drug_combinations": {
      "fields": [
        "id",
        "combination_name",
        "canonical_name",
        "combination_type",
        "primary_brand_id",
        "development_stage",
        "rationale",
        "combination_status",
        "data",
        "primary_source_id",
        "last_update_date"
      ],
      "description": "Drug combination therapies"
    },
    "drug_combination_components": {
      "fields": [
        "id",
        "combination_id",
        "drug_id",
        "role_in_combination",
        "ratio_or_dose",
        "data",
        "primary_source_id"
      ],
      "description": "Components of drug combinations"
    }
  },
  "Clinical_Module": {
    "clinical_trials": {
      "fields": [
        "id",
        "nct_id",
        "title",
        "status",
        "phase",
        "start_date",
        "completion_date",
        "planned_enrollment",
        "actual_enrollment",
        "primary_sponsor_id",
        "primary_registry_id",
        "primary_registry_identifier",
        "last_update_date",
        "data",
        "source_type",
        "primary_source_id",
        "termination_id",
        "termination_date"
      ],
      "description": "Clinical trials for drugs and therapies"
    },
    "clinical_trial_registries": {
      "fields": [
        "id",
        "registry_name",
        "registry_code",
        "managing_authority",
        "country_of_origin",
        "website_url",
        "api_available",
        "api_documentation_url",
        "data_update_frequency",
        "data_fields_available",
        "last_verified_date",
        "notes"
      ],
      "description": "Clinical trial registry information"
    },
    "formulation_details": {
      "fields": [
        "id",
        "drug_id",
        "combination_id",
        "form",
        "strength",
        "route_of_administration",
        "dosing_instructions",
        "excipients",
        "storage_requirements",
        "shelf_life",
        "last_update_date",
        "data",
        "primary_source_id"
      ],
      "description": "Drug formulation information"
    },
    "trial_registry_tracking": {
      "fields": [
        "id",
        "trial_id",
        "registry_id",
        "registry_specific_id",
        "registration_date",
        "last_updated_date",
        "registry_status",
        "registry_phase",
        "results_due_date",
        "results_posted_date",
        "has_results",
        "has_protocol",
        "compliance_status",
        "data_extraction_date",
        "raw_registry_data",
        "data",
        "primary_source_id"
      ],
      "description": "Trial registry tracking information"
    },
    "trial_registry_cross_references": {
      "fields": [
        "id",
        "source_registry_id",
        "source_trial_id",
        "target_registry_id",
        "target_trial_id",
        "cross_reference_date",
        "is_verified",
        "verification_method",
        "notes"
      ],
      "description": "Cross-references between trial registries"
    },
    "trial_identifiers": {
      "fields": [
        "id",
        "trial_id",
        "identifier_type",
        "identifier_value",
        "is_primary",
        "registry_id",
        "is_primary_registry",
        "source_type",
        "primary_source_id"
      ],
      "description": "Identifiers for clinical trials"
    },
    "clinical_trial_design": {
      "fields": [
        "id",
        "trial_id",
        "design_type",
        "blinding",
        "randomization_ratio",
        "control_type",
        "primary_objective",
        "secondary_objectives",
        "inclusion_criteria",
        "exclusion_criteria",
        "arms_description",
        "last_update_date",
        "primary_source_id"
      ],
      "description": "Design details for clinical trials"
    },
    "clinical_trial_arms": {
      "fields": [
        "id",
        "trial_id",
        "arm_name",
        "arm_type",
        "arm_description",
        "randomization_ratio",
        "is_control",
        "regimen_id",
        "planned_patients",
        "actual_patients",
        "last_update_date",
        "data",
        "primary_source_id"
      ],
      "description": "Trial arms information"
    },
    "clinical_trial_sites": {
      "fields": [
        "id",
        "trial_id",
        "site_name",
        "institution_name",
        "site_identifier",
        "principal_investigator",
        "pi_contact_info",
        "address_line1",
        "address_line2",
        "city",
        "state_province",
        "postal_code",
        "country",
        "geography_id",
        "latitude",
        "longitude",
        "site_type",
        "site_capabilities",
        "site_status",
        "activation_date",
        "closure_date",
        "data",
        "primary_source_id"
      ],
      "description": "Trial site information"
    },
    "clinical_trial_indications": {
      "fields": [
        "id",
        "trial_id",
        "disease_id",
        "indication_specification_id",
        "is_primary",
        "population_segment",
        "phase_specific",
        "data",
        "primary_source_id",
        "last_update_date"
      ],
      "description": "Disease indications for clinical trials"
    },
    "clinical_trial_drugs": {
      "fields": [
        "id",
        "trial_id",
        "drug_id",
        "role_in_trial",
        "is_lead_drug",
        "trial_aliases",
        "data",
        "primary_source_id"
      ],
      "description": "Drugs used in clinical trials"
    },
    "clinical_trial_geographies": {
      "fields": [
        "id",
        "trial_id",
        "geography_id",
        "regulatory_authority_id",
        "submission_date",
        "approval_date",
        "geography_status",
        "geography_specific_protocol",
        "protocol_differences",
        "geography_specific_budget",
        "geography_currency",
        "planned_sites",
        "active_sites",
        "planned_enrollment",
        "actual_enrollment",
        "first_site_activation_date",
        "last_site_activation_date",
        "first_patient_enrolled_date",
        "last_patient_enrolled_date",
        "enrollment_completed_date",
        "geography_specific_contact",
        "data",
        "primary_source_id"
      ],
      "description": "Geographic information for trials"
    },
    "trial_geography_regulatory_status": {
      "fields": [
        "id",
        "trial_geography_id",
        "status_date",
        "status_type",
        "status_details",
        "response_due_date",
        "response_submission_date",
        "reviewer_comments",
        "geography_specific_requirements",
        "data",
        "primary_source_id"
      ],
      "description": "Regulatory status for trial geographies"
    },
    "trial_enrollment_tracking": {
      "fields": [
        "id",
        "trial_id",
        "report_date",
        "disclosure_event_type",
        "cumulative_enrollment",
        "enrollment_percentage",
        "enrollment_status",
        "original_completion_date",
        "updated_completion_date",
        "timeline_status",
        "active_sites",
        "planned_sites",
        "site_status",
        "executive_comments",
        "notes",
        "primary_source_id"
      ],
      "description": "Enrollment tracking for trials"
    },
    "site_enrollment_tracking": {
      "fields": [
        "id",
        "site_id",
        "report_date",
        "planned_enrollment",
        "current_enrollment",
        "screening_failures",
        "completed_subjects",
        "discontinued_subjects",
        "discontinued_reasons",
        "enrollment_rate",
        "enrollment_percentage",
        "data",
        "primary_source_id"
      ],
      "description": "Enrollment tracking for sites"
    },
    "site_performance_metrics": {
      "fields": [
        "id",
        "site_id",
        "evaluation_period_start",
        "evaluation_period_end",
        "data_quality_score",
        "protocol_deviation_count",
        "serious_adverse_event_count",
        "query_resolution_time",
        "retention_rate",
        "site_monitoring_findings",
        "site_ranking",
        "key_performance_issues",
        "data"
      ],
      "description": "Performance metrics for trial sites"
    },
    "trial_vendors": {
      "fields": [
        "id",
        "trial_id",
        "vendor_company_id",
        "geography_id",
        "vendor_type",
        "scope_of_work",
        "contract_start_date",
        "contract_end_date",
        "vendor_status",
        "vendor_contact",
        "performance_rating",
        "data"
      ],
      "description": "Vendors for clinical trials"
    },
    "clinical_data_points": {
      "fields": [
        "id",
        "trial_id",
        "drug_id",
        "indication_id",
        "endpoint_type",
        "endpoint_name",
        "endpoint_category",
        "value",
        "statistical_significance",
        "p_value",
        "confidence_interval",
        "data",
        "last_update_date",
        "source_type",
        "primary_source_id"
      ],
      "description": "Clinical data points from trials"
    }
  },
  "Regulatory_Module": {
    "regulatory_authorities": {
      "fields": ["id", "name", "shortcode", "geography_id", "website", "data"],
      "description": "Regulatory authorities for drug approvals"
    },
    "regulatory_application_types": {
      "fields": [
        "id",
        "application_code",
        "application_name",
        "application_description",
        "applicable_product_types",
        "data"
      ],
      "description": "Types of regulatory applications"
    },
    "regulatory_review_pathways": {
      "fields": [
        "id",
        "pathway_code",
        "pathway_name",
        "pathway_description",
        "global_pathway_category",
        "typical_timeline_reduction",
        "qualifying_criteria",
        "data"
      ],
      "description": "Regulatory review pathways"
    },
    "authority_application_types": {
      "fields": [
        "id",
        "regulatory_authority_id",
        "application_type_id",
        "authority_specific_code",
        "local_name",
        "is_active",
        "requirements",
        "typical_timeline_days",
        "fee_amount",
        "fee_currency",
        "fee_year",
        "electronic_submission_portal",
        "guidance_document_url",
        "special_notes",
        "data"
      ],
      "description": "Application types for specific authorities"
    },
    "authority_review_pathways": {
      "fields": [
        "id",
        "regulatory_authority_id",
        "review_pathway_id",
        "authority_specific_code",
        "local_name",
        "is_active",
        "implementation_date",
        "statutory_timeline_days",
        "actual_average_timeline_days",
        "fee_implications",
        "special_requirements",
        "success_rate",
        "data"
      ],
      "description": "Review pathways for specific authorities"
    },
    "regulatory_submission_requirements": {
      "fields": [
        "id",
        "regulatory_authority_id",
        "application_type_id",
        "review_pathway_id",
        "requirement_category",
        "requirement_name",
        "requirement_description",
        "is_mandatory",
        "waiver_conditions",
        "format_requirements",
        "template_url",
        "guidance_reference",
        "notes",
        "effective_from",
        "effective_to",
        "data"
      ],
      "description": "Requirements for regulatory submissions"
    },
    "regulatory_designation_types": {
      "fields": [
        "id",
        "designation_code",
        "designation_name",
        "regulatory_authority_id",
        "designation_category",
        "typical_benefits",
        "qualifying_criteria",
        "exclusivity_period",
        "first_introduced_date",
        "is_active",
        "data"
      ],
      "description": "Types of regulatory designations"
    },
    "regulatory_submissions": {
      "fields": [
        "id",
        "drug_id",
        "indication_specification_id",
        "geography_id",
        "regulatory_authority_id",
        "application_type_id",
        "review_pathway_id",
        "submission_date",
        "submission_type",
        "submission_pathway",
        "receipt_confirmation_date",
        "status",
        "target_action_date",
        "actual_decision_date",
        "decision_outcome",
        "primary_source_id",
        "data"
      ],
      "description": "Regulatory submissions for drugs"
    },
    "regulatory_approvals": {
      "fields": [
        "id",
        "drug_id",
        "formulation_id",
        "indication_specification_id",
        "geography_id",
        "regulatory_authority_id",
        "approval_date",
        "approval_type",
        "approval_pathway",
        "approval_designations",
        "post_marketing_requirements",
        "conversion_to_full_approval_date",
        "withdrawal_date",
        "withdrawal_reason",
        "brand_name",
        "data",
        "primary_source_id"
      ],
      "description": "Regulatory approvals for drugs"
    },
    "regulatory_designations": {
      "fields": [
        "id",
        "drug_id",
        "indication_specification_id",
        "regulatory_authority_id",
        "geography_id",
        "designation_type",
        "status",
        "designation_date",
        "expiration_date",
        "renewal_date",
        "designation_benefits",
        "qualifying_criteria",
        "primary_source_id",
        "last_update_date",
        "data"
      ],
      "description": "Regulatory designations for drugs"
    },
    "regulatory_communications": {
      "fields": [
        "id",
        "drug_id",
        "indication_specification_id",
        "regulatory_authority_id",
        "geography_id",
        "communication_date",
        "communication_type",
        "communication_purpose",
        "key_outcomes",
        "next_steps",
        "impact_on_timeline",
        "primary_source_id",
        "last_update_date",
        "data"
      ],
      "description": "Communications with regulatory authorities"
    },
    "regulatory_exclusivity": {
      "fields": [
        "id",
        "drug_id",
        "indication_specification_id",
        "geography_id",
        "regulatory_authority_id",
        "exclusivity_type",
        "start_date",
        "end_date",
        "status",
        "last_update_date",
        "data",
        "primary_source_id"
      ],
      "description": "Exclusivity periods for drugs"
    },
    "regulatory_review_milestones": {
      "fields": [
        "id",
        "drug_id",
        "indication_specification_id",
        "geography_id",
        "regulatory_authority_id",
        "submission_id",
        "milestone_type",
        "milestone_date",
        "milestone_outcome",
        "adcom_vote_count",
        "review_division",
        "review_comments",
        "last_update_date",
        "data",
        "source_type",
        "primary_source_id"
      ],
      "description": "Milestones in regulatory reviews"
    },
    "standard_review_milestones": {
      "fields": [
        "id",
        "milestone_code",
        "milestone_name",
        "milestone_description",
        "global_milestone_category",
        "is_decision_point",
        "relative_day",
        "data"
      ],
      "description": "Standard milestones in regulatory reviews"
    },
    "authority_review_process_milestones": {
      "fields": [
        "id",
        "regulatory_authority_id",
        "application_type_id",
        "review_pathway_id",
        "milestone_id",
        "authority_specific_name",
        "relative_day",
        "is_publicly_disclosed",
        "has_statutory_deadline",
        "internal_significance",
        "notes",
        "data"
      ],
      "description": "Authority-specific review process milestones"
    },
    "patents": {
      "fields": [
        "id",
        "patent_number",
        "title",
        "filing_date",
        "issue_date",
        "expiration_date",
        "patent_type",
        "jurisdiction",
        "applicant",
        "assignee",
        "first_claim",
        "status",
        "last_update_date",
        "data",
        "source_type",
        "primary_source_id"
      ],
      "description": "Patent information for drugs"
    },
    "patent_litigation": {
      "fields": [
        "id",
        "patent_id",
        "case_number",
        "court",
        "filing_date",
        "plaintiff",
        "defendant",
        "status",
        "decision",
        "decision_date",
        "settlement_terms",
        "last_update_date",
        "data",
        "source_type",
        "primary_source_id"
      ],
      "description": "Patent litigation information"
    }
  },
  "Treatment_Module": {
    "regimens": {
      "fields": [
        "id",
        "name",
        "canonical_name",
        "primary_indication",
        "regimen_type",
        "guideline_reference",
        "guideline_category",
        "administration_cycle",
        "typical_duration",
        "last_update_date",
        "data",
        "source_type",
        "primary_source_id"
      ],
      "description": "Treatment regimens"
    },
    "regimen_components": {
      "fields": [
        "id",
        "regimen_id",
        "component_type",
        "drug_id",
        "combination_id",
        "administration_timing",
        "dosing_instructions",
        "sequence_order",
        "is_optional",
        "notes",
        "data",
        "primary_source_id"
      ],
      "description": "Components of treatment regimens"
    },
    "regimen_efficacy_comparisons": {
      "fields": [
        "id",
        "primary_regimen_id",
        "comparator_regimen_id",
        "disease_id",
        "comparison_type",
        "efficacy_metric",
        "primary_value",
        "comparator_value",
        "difference_value",
        "statistical_significance",
        "data_source_type",
        "source_study_id",
        "is_direct_comparison",
        "comparison_methodology",
        "last_update_date",
        "data",
        "primary_source_id"
      ],
      "description": "Efficacy comparisons between regimens"
    },
    "regimen_safety_comparisons": {
      "fields": [
        "id",
        "primary_regimen_id",
        "comparator_regimen_id",
        "disease_id",
        "safety_parameter",
        "parameter_category",
        "severity_grade",
        "primary_incidence_percentage",
        "comparator_incidence_percentage",
        "relative_risk",
        "hazard_ratio",
        "statistical_significance",
        "is_direct_comparison",
        "comparison_methodology",
        "data_source_type",
        "source_study_id",
        "clinical_relevance_assessment",
        "last_update_date",
        "data",
        "primary_source_id"
      ],
      "description": "Safety comparisons between regimens"
    },
    "combination_efficacy_comparisons": {
      "fields": [
        "id",
        "primary_combination_id",
        "comparator_combination_id",
        "disease_id",
        "comparison_type",
        "efficacy_metric",
        "primary_value",
        "comparator_value",
        "difference_value",
        "statistical_significance",
        "data_source_type",
        "source_study_id",
        "is_direct_comparison",
        "comparison_methodology",
        "last_update_date",
        "data",
        "primary_source_id"
      ],
      "description": "Efficacy comparisons between combinations"
    },
    "combination_safety_comparisons": {
      "fields": [
        "id",
        "primary_combination_id",
        "comparator_combination_id",
        "disease_id",
        "safety_parameter",
        "parameter_category",
        "severity_grade",
        "primary_incidence_percentage",
        "comparator_incidence_percentage",
        "relative_risk",
        "hazard_ratio",
        "statistical_significance",
        "is_direct_comparison",
        "comparison_methodology",
        "data_source_type",
        "source_study_id",
        "clinical_relevance_assessment",
        "last_update_date",
        "data",
        "primary_source_id"
      ],
      "description": "Safety comparisons between combinations"
    },
    "standard_of_care": {
      "fields": [
        "id",
        "disease_id",
        "geography_id",
        "regimen_id",
        "line_of_therapy",
        "patient_segment",
        "effective_from",
        "effective_until",
        "guideline_source",
        "guideline_version",
        "preference_level",
        "recommendation_strength",
        "notes",
        "last_update_date",
        "data",
        "primary_source_id"
      ],
      "description": "Standard of care information"
    }
  },
  "Commercial_Module": {
    "drug_brands": {
      "fields": [
        "id",
        "drug_id",
        "brand_name",
        "company_id",
        "geography_id",
        "regulatory_approval_id",
        "combination_id",
        "status",
        "data",
        "last_update_date",
        "primary_source_id"
      ],
      "description": "Brand information for drugs"
    },
    "brand_formulations": {
      "fields": [
        "id",
        "brand_id",
        "formulation_id",
        "packaging",
        "retail_package_size",
        "hospital_package_size",
        "ndc_code",
        "data",
        "primary_source_id"
      ],
      "description": "Formulations for drug brands"
    },
    "brand_company_relationships": {
      "fields": [
        "id",
        "brand_id",
        "company_id",
        "geography_id",
        "relationship_type",
        "exclusivity_type",
        "start_date",
        "end_date",
        "is_current",
        "role_description",
        "rights_from_company_id",
        "deal_id",
        "responsibilities",
        "data",
        "primary_source_id",
        "last_update_date"
      ],
      "description": "Company relationships with brands"
    },
    "manufacturing_relationships": {
      "fields": [
        "id",
        "drug_id",
        "combination_id",
        "formulation_id",
        "manufacturer_company_id",
        "rights_holder_company_id",
        "manufacturing_type",
        "geography_id",
        "facility_name",
        "facility_location",
        "start_date",
        "end_date",
        "is_current",
        "technology_transfer_status",
        "agreement_id",
        "data",
        "primary_source_id",
        "last_update_date"
      ],
      "description": "Manufacturing relationships for drugs"
    },
    "commercial_rights": {
      "fields": [
        "id",
        "drug_id",
        "company_id",
        "geography_id",
        "rights_type",
        "start_date",
        "end_date",
        "exclusivity",
        "royalty_terms",
        "rights_role",
        "relationship_status",
        "exclusivity_type",
        "territory_limitations",
        "agreement_reference",
        "rights_origin",
        "data",
        "primary_source_id"
      ],
      "description": "Commercial rights for drugs"
    },
    "sales_data": {
      "fields": [
        "id",
        "drug_id",
        "brand_id",
        "geography_id",
        "period_type",
        "period_value",
        "amount",
        "currency",
        "standardized_amount",
        "standardized_currency_id",
        "fx_rate_used",
        "fx_rate_date",
        "data",
        "primary_source_id"
      ],
      "description": "Sales data for drugs"
    },
    "market_sizing": {
      "fields": [
        "id",
        "disease_id",
        "geography_id",
        "year",
        "market_type",
        "patient_count",
        "revenue_value",
        "currency",
        "standardized_value",
        "standardized_currency_id",
        "fx_rate_used",
        "fx_rate_date",
        "growth_rate",
        "source_type",
        "forecast_methodology",
        "primary_source_id",
        "last_update_date",
        "data"
      ],
      "description": "Market sizing information"
    },
    "disease_epidemiology": {
      "fields": [
        "id",
        "disease_id",
        "geography_id",
        "year",
        "epidemiology_type",
        "patient_segment",
        "count_type",
        "patient_count",
        "primary_source_id",
        "last_update_date",
        "data"
      ],
      "description": "Disease epidemiology information"
    },
    "drug_market_forecasts": {
      "fields": [
        "id",
        "drug_id",
        "combination_id",
        "regimen_id",
        "disease_id",
        "indication_specification_id",
        "geography_id",
        "year",
        "forecast_type",
        "revenue_forecast",
        "patient_forecast",
        "market_share_forecast",
        "currency",
        "standardized_revenue_forecast",
        "standardized_currency_id",
        "treatment_rate",
        "forecast_scenario_id",
        "is_actual",
        "last_update_date",
        "data",
        "primary_source_id"
      ],
      "description": "Market forecasts for drugs"
    },
    "drug_pricing": {
      "fields": [
        "id",
        "drug_id",
        "formulation_id",
        "geography_id",
        "effective_date",
        "price_type",
        "price_value",
        "price_basis",
        "currency",
        "standardized_price_value",
        "standardized_currency_id",
        "fx_rate_used",
        "fx_rate_date",
        "reimbursement_status",
        "payer_type",
        "discount_percentage",
        "primary_source_id",
        "last_update_date",
        "data"
      ],
      "description": "Pricing information for drugs"
    },
    "competitive_landscape": {
      "fields": [
        "id",
        "disease_id",
        "geography_id",
        "year",
        "competitor_count",
        "market_leader_id",
        "leader_market_share",
        "barriers_to_entry",
        "competitive_intensity",
        "primary_source_id",
        "last_update_date",
        "data"
      ],
      "description": "Competitive landscape information"
    },
    "drug_market_positioning": {
      "fields": [
        "id",
        "drug_id",
        "indication_specification_id",
        "competitor_id",
        "comparison_dimension",
        "relative_position",
        "position_details",
        "evidence_strength",
        "primary_source_id",
        "last_update_date",
        "data"
      ],
      "description": "Market positioning for drugs"
    },
    "market_access_status": {
      "fields": [
        "id",
        "drug_id",
        "indication_specification_id",
        "geography_id",
        "launch_date",
        "launch_status",
        "access_level",
        "formulary_status",
        "prior_authorization",
        "patient_support_programs",
        "primary_source_id",
        "last_update_date",
        "data"
      ],
      "description": "Market access status for drugs"
    },
    "analyst_opinions": {
      "fields": [
        "id",
        "drug_id",
        "analyst_name",
        "firm_name",
        "opinion_date",
        "opinion_type",
        "rating",
        "forecast_value",
        "forecast_year",
        "opinion_text",
        "primary_source_id",
        "last_update_date",
        "data"
      ],
      "description": "Analyst opinions on drugs"
    },
    "market_catalysts": {
      "fields": [
        "id",
        "disease_id",
        "drug_id",
        "catalyst_date",
        "catalyst_type",
        "description",
        "impact_level",
        "entity_type",
        "entity_id",
        "probability",
        "geography_id",
        "regulatory_authority_id",
        "is_global",
        "geography_impact_level",
        "follow_on_geographies",
        "primary_source_id",
        "data",
        "last_update_date"
      ],
      "description": "Market catalysts information"
    },
    "catalyst_types": {
      "fields": [
        "id",
        "catalyst_category",
        "catalyst_type",
        "typical_lead_time",
        "typical_impact_duration",
        "geography_relevance",
        "description"
      ],
      "description": "Types of market catalysts"
    },
    "related_catalysts": {
      "fields": [
        "id",
        "source_catalyst_id",
        "related_catalyst_id",
        "relationship_type",
        "expected_time_gap",
        "relationship_strength",
        "notes",
        "primary_source_id"
      ],
      "description": "Relationships between catalysts"
    },
    "catalyst_impact_tracking": {
      "fields": [
        "id",
        "catalyst_id",
        "impact_metric",
        "pre_event_value",
        "post_event_value",
        "measurement_timeframe",
        "geography_id",
        "impact_description",
        "was_expected",
        "data_source",
        "data",
        "primary_source_id"
      ],
      "description": "Impact tracking for market catalysts"
    }
  },
  "Financial_Module": {
    "currencies": {
      "fields": [
        "id",
        "currency_code",
        "currency_name",
        "is_active",
        "decimal_places",
        "symbol"
      ],
      "description": "Currency reference information"
    },
    "exchange_rate_history": {
      "fields": [
        "id",
        "base_currency_id",
        "target_currency_id",
        "effective_date",
        "rate_value",
        "rate_source",
        "is_official",
        "is_eop",
        "is_average",
        "notes",
        "created_at",
        "created_by"
      ],
      "description": "Historical exchange rates"
    },
    "currency_settings": {
      "fields": [
        "id",
        "setting_name",
        "setting_context",
        "default_currency_id",
        "effective_from",
        "effective_to",
        "created_at",
        "created_by"
      ],
      "description": "Currency settings for system"
    },
    "company_financial_data": {
      "fields": [
        "id",
        "company_id",
        "standard_metric_type",
        "original_metric_name",
        "standard_period_type",
        "standard_period_value",
        "original_period_name",
        "period_start_date",
        "period_end_date",
        "amount",
        "original_currency",
        "standardized_currency",
        "standardized_amount",
        "fx_rate",
        "as_of_date",
        "confidence_score",
        "source_document",
        "extraction_notes",
        "data",
        "primary_source_id"
      ],
      "description": "Financial data for companies"
    },
    "financial_metric_synonyms": {
      "fields": [
        "id",
        "company_id",
        "original_term",
        "standard_term",
        "context",
        "confidence",
        "last_updated"
      ],
      "description": "Synonyms for financial metrics"
    },
    "financial_period_mappings": {
      "fields": [
        "id",
        "company_id",
        "original_period",
        "standard_period_type",
        "standard_period_value",
        "period_start_date",
        "period_end_date",
        "mapping_notes",
        "last_updated"
      ],
      "description": "Mappings for financial periods"
    },
    "company_fiscal_calendars": {
      "fields": [
        "id",
        "company_id",
        "fiscal_year_end_month",
        "fiscal_year_end_day",
        "quarters_alignment",
        "fiscal_year_notation",
        "effective_from",
        "effective_to"
      ],
      "description": "Fiscal calendars for companies"
    },
    "business_deals": {
      "fields": [
        "id",
        "deal_name",
        "deal_type",
        "status",
        "announcement_date",
        "closing_date",
        "start_date",
        "end_date",
        "upfront_payment",
        "upfront_currency",
        "standardized_upfront",
        "standardized_currency_id",
        "fx_rate_used",
        "fx_rate_date",
        "milestone_payments",
        "royalty_structure",
        "total_potential_value",
        "value_currency",
        "strategic_rationale",
        "portfolio_impact",
        "synergy_potential",
        "integration_plan",
        "company_acquirer_id",
        "company_target_id",
        "data",
        "is_multiparty",
        "is_partial_divestiture",
        "deal_structure",
        "tax_structure",
        "financing_structure",
        "primary_source_id",
        "last_update_date"
      ],
      "description": "Business deal information"
    },
    "investments": {
      "fields": [
        "id",
        "company_id",
        "investor_id",
        "investment_type",
        "amount",
        "currency",
        "standardized_amount",
        "standardized_currency_id",
        "fx_rate_used",
        "fx_rate_date",
        "investment_date",
        "post_money_valuation",
        "data",
        "primary_source_id"
      ],
      "description": "Investment information"
    },
    "transaction_parties": {
      "fields": [
        "id",
        "deal_id",
        "company_id",
        "party_role",
        "ownership_percentage",
        "investment_amount",
        "currency",
        "standardized_amount",
        "standardized_currency_id",
        "is_lead",
        "special_rights",
        "strategic_rationale",
        "data",
        "primary_source_id"
      ],
      "description": "Parties involved in transactions"
    },
    "transaction_assets": {
      "fields": [
        "id",
        "deal_id",
        "asset_type",
        "asset_name",
        "asset_description",
        "drug_id",
        "combination_id",
        "regimen_id",
        "research_program_id",
        "patent_id",
        "divesting_company_id",
        "acquiring_company_id",
        "asset_valuation",
        "valuation_methodology",
        "allocation_percentage",
        "facility_location",
        "employee_count",
        "annual_revenue",
        "product_stage",
        "therapeutic_areas",
        "territories_included",
        "exclusivity_expiration",
        "data",
        "primary_source_id"
      ],
      "description": "Assets involved in transactions"
    },
    "post_transaction_entity_changes": {
      "fields": [
        "id",
        "deal_id",
        "entity_type",
        "entity_id",
        "change_type",
        "resulted_in_entity_type",
        "resulted_in_entity_id",
        "change_date",
        "change_details",
        "data",
        "primary_source_id"
      ],
      "description": "Changes to entities after transactions"
    },
    "acquisition_consortiums": {
      "fields": [
        "id",
        "deal_id",
        "consortium_name",
        "lead_company_id",
        "formation_date",
        "legal_structure",
        "decision_making_process",
        "asset_allocation_agreement",
        "data"
      ],
      "description": "Consortiums for acquisitions"
    },
    "deal_stages": {
      "fields": [
        "id",
        "deal_id",
        "stage_type",
        "status",
        "start_date",
        "completion_date",
        "key_conditions",
        "regulatory_bodies",
        "notes",
        "primary_source_id"
      ],
      "description": "Stages of deals"
    },
    "partnership_details": {
      "fields": [
        "id",
        "deal_id",
        "geographic_scope",
        "therapeutic_areas",
        "product_scope",
        "development_responsibilities",
        "commercial_responsibilities",
        "manufacturing_responsibilities",
        "exclusivity_terms",
        "ip_ownership_terms",
        "governance_structure",
        "decision_making_process",
        "term_extension_conditions",
        "termination_triggers",
        "data",
        "last_update_date"
      ],
      "description": "Details of partnerships"
    },
    "deal_financial_components": {
      "fields": [
        "id",
        "deal_id",
        "component_type",
        "component_name",
        "trigger_description",
        "potential_value",
        "currency",
        "standardized_value",
        "standardized_currency_id",
        "probability",
        "estimated_timing",
        "is_disclosed",
        "achievement_status",
        "actual_payment_date",
        "actual_payment_amount",
        "notes"
      ],
      "description": "Financial components of deals"
    },
    "deal_amendments": {
      "fields": [
        "id",
        "deal_id",
        "amendment_date",
        "amendment_type",
        "description",
        "changed_terms",
        "reason_for_change",
        "financial_impact",
        "primary_source_id"
      ],
      "description": "Amendments to deals"
    },
    "licensing_details": {
      "fields": [
        "id",
        "deal_id",
        "license_type",
        "field_of_use",
        "territory_scope",
        "sublicensing_rights",
        "technology_transfer_terms",
        "diligence_obligations",
        "patent_rights_included",
        "know_how_rights_included",
        "improvement_rights",
        "prosecution_responsibilities",
        "term_and_termination",
        "data_reporting_requirements",
        "regulatory_responsibilities",
        "notes",
        "data"
      ],
      "description": "Details of licensing agreements"
    },
    "investment_funds": {
      "fields": [
        "id",
        "fund_name",
        "company_id",
        "fund_type",
        "vintage_year",
        "fund_size",
        "fund_size_currency",
        "standardized_fund_size",
        "standardized_currency_id",
        "fund_number",
        "investment_stage_focus",
        "therapeutic_focus",
        "geographic_focus",
        "closing_date",
        "investment_period_end",
        "fund_life_end",
        "management_fees",
        "notes",
        "data",
        "primary_source_id"
      ],
      "description": "Investment fund information"
    },
    "investment_rounds": {
      "fields": [
        "id",
        "company_id",
        "round_name",
        "announcement_date",
        "closing_date",
        "pre_money_valuation",
        "post_money_valuation",
        "total_raised",
        "currency",
        "standardized_total_raised",
        "standardized_currency_id",
        "is_crossover",
        "is_extension",
        "extension_of_round_id",
        "lead_investor_id",
        "bank_or_advisor",
        "use_of_proceeds",
        "notes",
        "primary_source_id",
        "data"
      ],
      "description": "Investment round information"
    },
    "round_participants": {
      "fields": [
        "id",
        "round_id",
        "investor_id",
        "investment_fund_id",
        "amount",
        "currency",
        "standardized_amount",
        "standardized_currency_id",
        "is_lead",
        "is_new_investor",
        "participation_type",
        "resulting_ownership_percentage",
        "board_seat_gained",
        "board_observer_rights",
        "special_rights",
        "notes"
      ],
      "description": "Participants in investment rounds"
    },
    "investment_instruments": {
      "fields": [
        "id",
        "round_id",
        "instrument_type",
        "amount",
        "currency",
        "standardized_amount",
        "standardized_currency_id",
        "interest_rate",
        "discount_rate",
        "valuation_cap",
        "conversion_trigger",
        "maturity_date",
        "liquidation_preference",
        "participation_rights",
        "anti_dilution_protection",
        "special_terms",
        "notes",
        "data"
      ],
      "description": "Investment instruments information"
    },
    "forecast_projects": {
      "fields": [
        "id",
        "project_name",
        "creation_date",
        "author",
        "forecast_owner",
        "forecast_type",
        "time_horizon",
        "forecast_status",
        "methodology",
        "key_assumptions",
        "superseded_by_id",
        "base_case_scenario_id",
        "data",
        "primary_source_id",
        "last_update_date"
      ],
      "description": "Forecast project information"
    },
    "forecast_scenarios": {
      "fields": [
        "id",
        "forecast_project_id",
        "scenario_name",
        "scenario_type",
        "scenario_probability",
        "description",
        "key_assumptions",
        "last_update_date",
        "data",
        "primary_source_id"
      ],
      "description": "Forecast scenario information"
    },
    "forecast_accuracy_analysis": {
      "fields": [
        "id",
        "forecast_scenario_id",
        "entity_type",
        "entity_id",
        "metric_type",
        "forecast_period",
        "forecast_value",
        "actual_value",
        "absolute_difference",
        "percentage_difference",
        "analysis_date",
        "analysis_notes",
        "data",
        "primary_source_id"
      ],
      "description": "Analysis of forecast accuracy"
    },
    "forecast_drivers": {
      "fields": [
        "id",
        "forecast_scenario_id",
        "driver_category",
        "driver_name",
        "driver_description",
        "value_type",
        "baseline_value",
        "projected_values",
        "driver_impact_description",
        "sensitivity_level",
        "data_source",
        "data",
        "primary_source_id"
      ],
      "description": "Drivers for forecasts"
    },
    "forecast_model_changes": {
      "fields": [
        "id",
        "forecast_project_id",
        "change_date",
        "changed_by",
        "change_type",
        "change_description",
        "reason_for_change",
        "impact_on_forecast",
        "previous_value",
        "new_value",
        "data",
        "primary_source_id"
      ],
      "description": "Changes to forecast models"
    }
  },
  "Research_Evidence_Module": {
    "scientific_events": {
      "fields": [
        "id",
        "name",
        "acronym",
        "event_type",
        "start_date",
        "end_date",
        "location_city",
        "location_country",
        "organizing_body",
        "website_url",
        "importance_tier",
        "recurring_event_id",
        "data",
        "last_update_date",
        "primary_source_id"
      ],
      "description": "Scientific event information"
    },
    "scientific_publications": {
      "fields": [
        "id",
        "publication_type",
        "research_phase",
        "title",
        "authors",
        "first_author",
        "last_author",
        "corresponding_author",
        "journal_name",
        "publisher",
        "publication_date",
        "doi",
        "pmid",
        "open_access",
        "impact_factor",
        "citation_count",
        "is_peer_reviewed",
        "abstract",
        "full_text_available",
        "preprint_server",
        "preprint_doi",
        "preprint_version",
        "preprint_posted_date",
        "publication_status",
        "review_status",
        "review_timeline",
        "data",
        "document_source_id",
        "primary_source_id",
        "last_update_date"
      ],
      "description": "Scientific publication information"
    },
    "entity_publications": {
      "fields": [
        "id",
        "publication_id",
        "entity_type",
        "entity_id",
        "relationship_type",
        "publication_rank",
        "supersedes_publication_id",
        "document_source_id",
        "data",
        "last_update_date"
      ],
      "description": "Relationships between entities and publications"
    },
    "research_program_publication_details": {
      "fields": [
        "id",
        "entity_publication_id",
        "research_stage",
        "model_systems",
        "key_findings",
        "technology_platforms_used",
        "data_cutoff_date",
        "data",
        "last_update_date"
      ],
      "description": "Publication details for research programs"
    },
    "clinical_trial_publication_details": {
      "fields": [
        "id",
        "entity_publication_id",
        "publication_type",
        "data_cutoff_date",
        "follow_up_duration",
        "is_primary_analysis",
        "is_interim_analysis",
        "is_final_analysis",
        "data",
        "last_update_date"
      ],
      "description": "Publication details for clinical trials"
    },
    "publication_target_details": {
      "fields": [
        "id",
        "entity_publication_id",
        "target_role",
        "evidence_type",
        "cellular_context",
        "in_vivo_models",
        "key_findings",
        "data",
        "last_update_date"
      ],
      "description": "Target details in publications"
    },
    "publication_versions": {
      "fields": [
        "id",
        "preprint_publication_id",
        "final_publication_id",
        "relationship_type",
        "transition_date",
        "significant_changes",
        "data",
        "primary_source_id"
      ],
      "description": "Relationships between publication versions"
    },
    "publication_altmetrics": {
      "fields": [
        "id",
        "publication_id",
        "metric_type",
        "metric_value",
        "collection_date",
        "source",
        "data",
        "primary_source_id"
      ],
      "description": "Alternative metrics for publications"
    },
    "scientific_presentations": {
      "fields": [
        "id",
        "entity_publication_id",
        "presentation_date",
        "presentation_type",
        "presentation_id",
        "presenter_name",
        "presenter_affiliation",
        "event_id",
        "presentation_title",
        "key_findings",
        "has_new_data",
        "presentation_materials_available",
        "document_source_id",
        "data",
        "last_update_date",
        "primary_source_id"
      ],
      "description": "Scientific presentation information"
    },
    "publication_analysis_sets": {
      "fields": [
        "id",
        "publication_id",
        "analysis_set_name",
        "analysis_set_description",
        "patient_count",
        "is_primary",
        "analysis_set_criteria",
        "data",
        "last_update_date",
        "primary_source_id"
      ],
      "description": "Analysis sets in publications"
    },
    "publication_study_arms": {
      "fields": [
        "id",
        "publication_id",
        "arm_name",
        "arm_description",
        "treatment_description",
        "is_control",
        "patient_count",
        "corresponds_to_trial_arm_id",
        "data",
        "last_update_date",
        "primary_source_id"
      ],
      "description": "Study arms in publications"
    },
    "publication_results": {
      "fields": [
        "id",
        "publication_id",
        "result_type",
        "endpoint_name",
        "endpoint_definition",
        "analysis_set_id",
        "arm_id",
        "comparator_arm_id",
        "is_comparative",
        "result_value",
        "statistical_significance",
        "p_value",
        "confidence_interval",
        "effect_size",
        "timepoint",
        "result_hierarchy",
        "parent_result_id",
        "importance_rank",
        "differs_from_protocol",
        "is_post_hoc",
        "data",
        "last_update_date",
        "primary_source_id"
      ],
      "description": "Results reported in publications"
    },
    "publication_result_graphics": {
      "fields": [
        "id",
        "publication_id",
        "figure_number",
        "figure_title",
        "figure_caption",
        "figure_type",
        "related_endpoints",
        "image_path",
        "document_location_id",
        "data",
        "last_update_date",
        "primary_source_id"
      ],
      "description": "Graphics in publication results"
    },
    "publication_subgroup_analyses": {
      "fields": [
        "id",
        "publication_id",
        "parent_result_id",
        "subgroup_type",
        "subgroup_criteria",
        "subgroup_size",
        "is_prespecified",
        "interaction_p_value",
        "forest_plot_figure_id",
        "data",
        "last_update_date",
        "primary_source_id"
      ],
      "description": "Subgroup analyses in publications"
    },
    "people": {
      "fields": [
        "id",
        "name",
        "linkedin_url",
        "personal_email",
        "phone",
        "therapeutic_focus",
        "functional_expertise",
        "background",
        "last_update_date",
        "data",
        "source_type",
        "primary_source_id"
      ],
      "description": "People information"
    },
    "employment": {
      "fields": [
        "id",
        "person_id",
        "company_id",
        "title",
        "department",
        "role_type",
        "company_email",
        "company_phone",
        "start_date",
        "end_date",
        "is_current",
        "is_primary_contact",
        "last_update_date",
        "data",
        "source_type",
        "primary_source_id"
      ],
      "description": "Employment information"
    },
    "expertise_areas": {
      "fields": [
        "id",
        "name",
        "canonical_name",
        "expertise_type",
        "parent_expertise_id",
        "data"
      ],
      "description": "Areas of expertise"
    },
    "person_expertise": {
      "fields": [
        "id",
        "person_id",
        "expertise_id",
        "proficiency_level",
        "years_experience",
        "is_primary",
        "data",
        "last_update_date",
        "primary_source_id"
      ],
      "description": "Expertise of people"
    }
  },
  "Lifecycle_Events_Module": {
    "entity_milestones": {
      "fields": [
        "id",
        "entity_type",
        "entity_id",
        "milestone_type_id",
        "milestone_category",
        "milestone_name",
        "planned_date",
        "actual_date",
        "status",
        "delay_reason",
        "geography_id",
        "company_id",
        "significance",
        "public_disclosure_date",
        "disclosure_source_id",
        "next_milestone_id",
        "dependencies",
        "impact_on_valuation",
        "data",
        "primary_source_id",
        "last_update_date"
      ],
      "description": "Milestones for entities"
    },
    "milestone_types": {
      "fields": [
        "id",
        "milestone_category",
        "milestone_type",
        "applicable_entity_types",
        "typical_timeline",
        "is_public",
        "significance_level",
        "description"
      ],
      "description": "Types of milestones"
    },
    "program_terminations": {
      "fields": [
        "id",
        "termination_date",
        "research_program_id",
        "drug_id",
        "combination_id",
        "regimen_id",
        "clinical_trial_id",
        "indication_id",
        "indication_specification_id",
        "terminating_company_id",
        "development_stage",
        "termination_type",
        "specific_reasons",
        "decision_trigger",
        "decision_data_reference_id",
        "was_anticipated",
        "impact_level",
        "disclosure_date",
        "disclosure_vehicle",
        "official_rationale",
        "pipeline_impact",
        "financial_impact",
        "headcount_impact",
        "facility_impact",
        "asset_disposition",
        "successor_program_id",
        "out_licensed_to_id",
        "data",
        "primary_source_id",
        "last_update_date"
      ],
      "description": "Program termination information"
    },
    "termination_data_points": {
      "fields": [
        "id",
        "termination_id",
        "data_type",
        "metric_name",
        "observed_value",
        "threshold_value",
        "significance",
        "data_source",
        "impact_weight",
        "notes",
        "data",
        "primary_source_id"
      ],
      "description": "Data points for terminations"
    },
    "termination_pattern_analysis": {
      "fields": [
        "id",
        "analysis_date",
        "analysis_type",
        "analysis_scope",
        "time_period_start",
        "time_period_end",
        "total_terminations",
        "total_active_programs",
        "termination_rate",
        "benchmark_comparison",
        "stage_distribution",
        "reason_distribution",
        "key_insights",
        "data",
        "primary_source_id",
        "last_update_date"
      ],
      "description": "Analysis of termination patterns"
    }
  },
  "Metadata_Tracking_Module": {
    "entity_versions": {
      "fields": [
        "id",
        "entity_type",
        "entity_id",
        "version_number",
        "changed_by",
        "change_reason",
        "previous_data",
        "current_data",
        "change_timestamp"
      ],
      "description": "Version history for entities"
    },
    "schema_evolution": {
      "fields": [
        "id",
        "entity_type",
        "json_path",
        "description",
        "value_type",
        "occurrence_count",
        "first_seen",
        "last_seen",
        "is_active"
      ],
      "description": "Schema evolution tracking"
    },
    "entity_resolution_log": {
      "fields": [
        "id",
        "timestamp",
        "entity_type",
        "entity_id",
        "source_entity",
        "resolution_action",
        "confidence",
        "reasoning"
      ],
      "description": "Entity resolution log"
    },
    "data_source_metadata": {
      "fields": [
        "id",
        "source_name",
        "source_type",
        "entity_types_found",
        "common_fields",
        "quality_assessment",
        "last_ingested",
        "ingestion_frequency",
        "example_entities"
      ],
      "description": "Metadata about data sources"
    },
    "query_analytics": {
      "fields": [
        "id",
        "query_pattern",
        "entity_types_queried",
        "fields_queried",
        "frequency",
        "last_queried",
        "avg_confidence",
        "missing_data_notes"
      ],
      "description": "Analytics for queries"
    }
  }
}