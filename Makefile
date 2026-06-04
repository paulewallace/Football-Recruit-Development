.PHONY: ingest match transform app pipeline

pipeline: ingest match transform

ingest:
	python3 -m python.ingest.pull_recruits
	python3 -m python.ingest.pull_nfl_draft
	python3 -m python.ingest.pull_program_ref
	python3 -m python.ingest.pull_transfers

match:
	python3 -m python.matching.build_player_bridge
	python3 -m python.matching.build_school_timeline

transform:
	python3 -m python.run_transform

app:
	python3 -m python.run_app
