import os
import json
from datetime import datetime


class SessionEngine:
    """
    CRME Session Engine v1.5

    Responsibilities:
    - Create research sessions
    - Store session state
    - Manage research memory
    - Generate human-readable research reports
    - Maintain research provenance
    """

    def __init__(
        self,
        base_path,
        project=None
    ):

        self.base_path = base_path
        self.project = project

        self.session_dir = os.path.join(
            base_path,
            "memory",
            "sessions"
        )

        os.makedirs(
            self.session_dir,
            exist_ok=True
        )


    # =====================================================
    # CREATE SESSION
    # =====================================================

    def create_session(
        self,
        project_id=None,
        metadata=None
    ):

        session_id = (
            f"S-{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"
        )

        now = datetime.utcnow().isoformat()

        session = {

            "session_id": session_id,

            "project_id": project_id,

            "created_at": now,

            "updated_at": now,

            "metadata": metadata or {},


            "state": {

                "messages": [],

                "decisions": [],

                "goals": [],

                "artifacts": [],

                "notes": []

            },


            "research": {

                "summary": "",

                "ledger": [],

                "decisions": [],

                "ideas": [],

                "provenance": [],

                "next_goal": ""

            },


            "version": 2
        }


        self.save_session(
            session_id,
            session
        )


        return session_id



    # =====================================================
    # LOAD SESSION
    # =====================================================

    def load_session(
        self,
        session_id
    ):

        return self.get_snapshot(
            session_id
        )



    # =====================================================
    # UPDATE SESSION
    # =====================================================

    def update_session(
        self,
        session_id,
        update
    ):

        session = self.load_session(
            session_id
        )


        if not session:
            return False


        state = session.get(
            "state",
            {}
        )


        for key, value in update.items():

            if key in state and isinstance(
                state[key],
                list
            ):

                if isinstance(value, list):

                    state[key].extend(value)

                else:

                    state[key].append(value)

            else:

                state[key] = value



        session["state"] = state

        session["updated_at"] = (
            datetime.utcnow().isoformat()
        )


        session["version"] += 1


        self.save_session(
            session_id,
            session
        )


        return True



    # =====================================================
    # SAVE SESSION
    # =====================================================

    def save_session(
        self,
        session_id,
        data
    ):

        path = os.path.join(
            self.session_dir,
            f"{session_id}.json"
        )


        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=2,
                ensure_ascii=False
            )



    # =====================================================
    # GET SNAPSHOT
    # =====================================================

    def get_snapshot(
        self,
        session_id
    ):

        path = os.path.join(
            self.session_dir,
            f"{session_id}.json"
        )


        if not os.path.exists(path):

            return None


        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)



    # =====================================================
    # BUILD RESEARCH SUMMARY
    # =====================================================

    def build_summary(
        self,
        session
    ):

        state = session.get(
            "state",
            {}
        )


        summary = (

            f"Session {session['session_id']} "

            f"contains "

            f"{len(state.get('messages', []))} messages, "

            f"{len(state.get('decisions', []))} decisions, "

            f"{len(state.get('goals', []))} goals."

        )


        return summary



    # =====================================================
    # GENERATE MARKDOWN REPORT
    # =====================================================

    def generate_markdown_report(
        self,
        session_id
    ):

        session = self.load_session(
            session_id
        )


        if not session:

            return None



        research = session.get(
            "research",
            {}
        )


        path = os.path.join(
            self.session_dir,
            f"{session_id}.md"
        )


        content = f"""
# CRME Research Session Report


## Session Metadata

Session ID:
{session.get('session_id')}

Project:
{session.get('project_id')}

Created:
{session.get('created_at')}



## Research Summary

{research.get('summary')}



## Research Ledger Entry

"""

        for item in research.get("ledger", []):

            content += f"- {item}\n"


        content += """



## Decision Log Entry

"""


        for item in research.get("decisions", []):

            content += f"- {item}\n"


        content += """



## Idea Inbox Entry

"""


        for item in research.get("ideas", []):

            content += f"- {item}\n"


        content += """



## Research Provenance

"""


        for item in research.get("provenance", []):

            content += f"- {item}\n"


        content += f"""



## Next Session Goal

{research.get('next_goal')}

"""


        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(content)


        return path



    # =====================================================
    # FINALIZE SESSION
    # =====================================================

    def finalize_session(
        self,
        session_id
    ):

        session = self.load_session(
            session_id
        )


        if not session:

            return False


        session["research"]["summary"] = (
            self.build_summary(session)
        )


        session["updated_at"] = (
            datetime.utcnow().isoformat()
        )


        self.save_session(
            session_id,
            session
        )


        report = self.generate_markdown_report(
            session_id
        )


        return {

            "session": session_id,

            "report": report

        }



    # =====================================================
    # LIST SESSIONS
    # =====================================================

    def list_sessions(self):

        sessions = []


        for file in os.listdir(
            self.session_dir
        ):

            if file.endswith(".json"):

                sid = file.replace(
                    ".json",
                    ""
                )


                snapshot = self.get_snapshot(
                    sid
                )


                if snapshot:

                    sessions.append(snapshot)


        return sessions



    # =====================================================
    # BIND PROJECT
    # =====================================================

    def bind_to_project(
        self,
        session_id,
        project_id
    ):

        session = self.load_session(
            session_id
        )


        if not session:

            return False


        session["project_id"] = project_id


        session["updated_at"] = (
            datetime.utcnow().isoformat()
        )


        self.save_session(
            session_id,
            session
        )


        return True

