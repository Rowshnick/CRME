import os
import json
from datetime import datetime


class ContextExporter:
    """
    CRME Context Export Layer v1.1

    Features:
    - LLM independent context transfer
    - Research snapshot export
    - Project brief generation
    - Export manifest creation
    """


    def __init__(
        self,
        project_engine,
        session_engine,
        graph_engine
    ):

        self.project_engine = project_engine
        self.session_engine = session_engine
        self.graph_engine = graph_engine


        # Standard export structure

        self.export_root = "exports"

        self.snapshot_dir = os.path.join(
            self.export_root,
            "snapshots"
        )

        self.brief_dir = os.path.join(
            self.export_root,
            "briefs"
        )

        self.package_dir = os.path.join(
            self.export_root,
            "packages"
        )


        self._prepare_directories()



    # =====================================================
    # DIRECTORY INITIALIZATION
    # =====================================================

    def _prepare_directories(self):

        for path in [
            self.snapshot_dir,
            self.brief_dir,
            self.package_dir
        ]:

            os.makedirs(
                path,
                exist_ok=True
            )



    # =====================================================
    # BUILD CONTEXT
    # =====================================================

    def build(self):

        return {

            "metadata": {

                "system":
                    "CRME",

                "version":
                    "Context Export v1.1",

                "created_at":
                    datetime.utcnow().isoformat()

            },


            "project":
                self.project_engine.to_dict(),


            "summary":
                self.project_engine.summary(),


            "decisions":
                self.project_engine.decision_log,


            "research_ledger":
                self.project_engine.research_ledger,


            "knowledge_graph":
                self.graph_engine.export(),


            "sessions":
                self._export_sessions(),


            "transfer_info": {

                "current_stage":
                    "Core Integration Completed",

                "next_stage":
                    "Semantic Query Engine",

                "purpose":
                    "Transfer CRME state between LLM systems"

            }

        }



    # =====================================================
    # SESSION EXPORT
    # =====================================================

    def _export_sessions(self):

        sessions = []

        path = self.session_engine.session_dir


        if os.path.exists(path):

            for file in os.listdir(path):

                if file.endswith(".json"):

                    with open(
                        os.path.join(path,file),
                        "r",
                        encoding="utf-8"
                    ) as f:

                        sessions.append(
                            json.load(f)
                        )

        return sessions



    # =====================================================
    # SAVE SNAPSHOT
    # =====================================================

    def save_snapshot(
        self,
        filename="CRME_Context_Snapshot_v1.1.json"
    ):

        path = os.path.join(
            self.snapshot_dir,
            filename
        )


        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.build(),
                f,
                indent=2,
                ensure_ascii=False
            )


        self.save_manifest()

        return path



    # =====================================================
    # SAVE PROJECT BRIEF
    # =====================================================

    def save_brief(
        self,
        filename="CRME_PROJECT_BRIEF.md"
    ):


        path = os.path.join(
            self.brief_dir,
            filename
        )


        summary = self.project_engine.summary()


        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
f"""# CRME Project Brief

## Project

{summary.get('project')}


## Status

{summary.get('status')}


## Progress

{summary.get('progress')}%


## Research Metrics

Sessions:
{summary.get('sessions')}

Decisions:
{summary.get('decisions')}

Knowledge Nodes:
{summary.get('knowledge_nodes')}


## Next Stage

Semantic Query Engine


## Transfer

This document is generated for
LLM-independent research context transfer.
"""
            )


        self.save_manifest()

        return path



    # =====================================================
    # EXPORT MANIFEST
    # =====================================================

    def save_manifest(self):


        manifest = {

            "system":
                "CRME",

            "version":
                "1.1",

            "created_at":
                datetime.utcnow().isoformat(),

            "project":
                self.project_engine.title,


            "exports": {

                "snapshot":
                    True,

                "brief":
                    True

            },


            "ready_for_llm_transfer":
                True

        }



        path = os.path.join(
            self.export_root,
            "CRME_EXPORT_MANIFEST.json"
        )


        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                manifest,
                f,
                indent=2,
                ensure_ascii=False
            )


        return path

