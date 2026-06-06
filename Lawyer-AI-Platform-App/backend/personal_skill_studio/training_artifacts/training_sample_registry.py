from personal_skill_studio.training_artifacts.schemas import TrainingSampleSegment


def summarize_segments(segments: list[TrainingSampleSegment]) -> dict:
    fact_segments = [segment for segment in segments if segment.target_skill_id == "case_fact_extraction_skill"]
    legal_segments = [segment for segment in segments if segment.target_skill_id == "case_legal_analysis_skill"]
    return {
        "segment_count": len(segments),
        "fact_segment_count": len(fact_segments),
        "legal_segment_count": len(legal_segments),
        "segment_types": [segment.segment_type for segment in segments],
        "metadata_only": True,
        "raw_content_included": False,
        "redaction_completed": all(segment.redaction_completed for segment in segments) if segments else False,
    }
