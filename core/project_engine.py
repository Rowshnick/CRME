import json
import os
from datetime import datetime



class ResearchProject:
    """
    CRME Research Project Engine

    Responsible for:

    - Project lifecycle
    - Research ledger
    - Decision tracking
    - Idea management
    - Knowledge graph synchronization
    - Persistent project state
    """



    def __init__(
        self,
        project_id,
        title,
        description="",
        paper_target="Q1",
        repository="",
        tags=None
    ):


        self.project_id = project_id

        self.title = title

        self.description = description

        self.paper_target = paper_target

        self.repository = repository


        self.status = "Active"

        self.current_phase = "Initialization"



        now = datetime.utcnow().isoformat()


        self.created_at = now

        self.updated_at = now



        self.progress = 0



        self.sessions = []

        self.milestones = []

        self.publications = []



        self.research_ledger = []

        self.decision_log = []

        self.idea_inbox = []

        self.provenance_log = []



        self.dependencies = []


        self.tags = tags or []



        self.knowledge_metrics = {

            "nodes": 0,

            "relations": 0,

            "memories": 0

        }




    # =====================================================
    # SESSION EVENT
    # =====================================================

    def handle_session_event(
        self,
        event_type,
        payload
    ):


        timestamp = datetime.utcnow().isoformat()


        session_id = payload.get(
            "session_id"
        )


        state = payload.get(
            "state",
            {}
        )


        if event_type == "session_created":


            if session_id not in self.sessions:

                self.sessions.append(
                    session_id
                )



        if event_type == "session_updated":


            for decision in state.get(
                "decisions",
                []
            ):

                self.decision_log.append(

                    {
                        "decision": decision,
                        "session_id": session_id,
                        "timestamp": timestamp
                    }

                )



            for goal in state.get(
                "goals",
                []
            ):

                self.idea_inbox.append(

                    {
                        "idea": goal,
                        "session_id": session_id,
                        "status": "open",
                        "timestamp": timestamp
                    }

                )



        self.research_ledger.append(

            {

                "event":
                    event_type,

                "session_id":
                    session_id,

                "timestamp":
                    timestamp

            }

        )


        self.updated_at = timestamp


        self._auto_update_progress()



    # =====================================================
    # GRAPH METRICS
    # =====================================================

    def update_graph_metrics(
        self,
        graph_data
    ):

        self.knowledge_metrics = {

            "nodes":
                len(
                    graph_data.get(
                        "objects",
                        []
                    )
                ),

            "relations":
                len(
                    graph_data.get(
                        "relations",
                        []
                    )
                ),

            "memories":
                len(
                    [
                        x for x in graph_data.get(
                            "objects",
                            []
                        )
                        if x.get("type") == "memory"
                    ]
                )

        }



    # =====================================================
    # GRAPH INTELLIGENCE SYNC
    # =====================================================

    def update_graph_knowledge(
        self,
        graph_data
    ):


        self.update_graph_metrics(
            graph_data
        )


        objects = graph_data.get(
            "objects",
            []
        )


        self.decision_log = []

        self.idea_inbox = []



        for obj in objects:


            obj_type = obj.get(
                "type"
            )


            data = obj.get(
                "data",
                {}
            )


            text = data.get(
                "text",
                ""
            )



            if obj_type == "decision":


                self.decision_log.append(

                    {

                        "decision":
                            text,

                        "source":
                            "graph"

                    }

                )



            elif obj_type == "goal":


                self.idea_inbox.append(

                    {

                        "idea":
                            text,

                        "source":
                            "graph",

                        "status":
                            "open"

                    }

                )



            elif obj_type == "artifact":


                self.provenance_log.append(

                    {

                        "artifact":
                            text,

                        "source":
                            "graph"

                    }

                )



        self.updated_at = (
            datetime.utcnow().isoformat()
        )




    # =====================================================
    # PROGRESS
    # =====================================================

    def _auto_update_progress(
        self
    ):


        self.progress = min(

            100,

            len(self.sessions) * 5

        )



    # =====================================================
    # SERIALIZATION
    # =====================================================

    def to_dict(
        self
    ):

        return self.__dict__



    def save(
        self,
        directory="storage"
    ):


        os.makedirs(
            directory,
            exist_ok=True
        )


        path = os.path.join(
            directory,
            "project.json"
        )


        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:


            json.dump(
                self.to_dict(),
                f,
                indent=2,
                ensure_ascii=False
            )


        return path




    @staticmethod
    def load(
        path
    ):


        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)



        obj = ResearchProject(

            data["project_id"],

            data["title"]

        )


        obj.__dict__.update(
            data
        )


        return obj




    # =====================================================
    # SUMMARY
    # =====================================================

    def summary(
        self
    ):


        return {

            "project":
                self.title,

            "status":
                self.status,

            "phase":
                self.current_phase,

            "progress":
                self.progress,

            "sessions":
                len(self.sessions),

            "goals":
                len(self.idea_inbox),

            "artifacts":
                len(self.provenance_log),

            "milestones":
                len(self.milestones),

            "ledger_entries":
                len(self.research_ledger),

            "decisions":
                len(self.decision_log),

            "ideas":
                len(self.idea_inbox),

            "knowledge_nodes":
                self.knowledge_metrics.get(
                    "nodes",
                    0
                )

        }

