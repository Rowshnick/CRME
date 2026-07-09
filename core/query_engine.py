import datetime


class QueryEngine:
    """
    CRME Semantic Intelligence Query Engine v1.0

    Integrates:

    - Graph Knowledge
    - Project Intelligence
    - Memory Objects
    - Research Decisions
    - Goals
    - Artifacts
    """



    def __init__(
        self,
        project,
        graph,
        memory=None
    ):

        self.project = project
        self.graph = graph
        self.memory = memory



    # =====================================================
    # MAIN QUERY
    # =====================================================

    def query(
        self,
        text
    ):

        text = text.lower()


        if "decision" in text:

            return self.search_type(
                "decision"
            )


        if "goal" in text:

            return self.search_type(
                "goal"
            )


        if "artifact" in text or "file" in text:

            return self.search_type(
                "artifact"
            )


        if "memory" in text:

            return self.search_type(
                "memory"
            )


        if "summary" in text:

            return self.project.summary()



        if "next" in text:

            return self.next_steps()



        return self.semantic_search(
            text
        )



    # =====================================================
    # SEARCH GRAPH
    # =====================================================

    def search_type(
        self,
        obj_type
    ):


        result = []


        data = self.graph.export()


        for obj in data.get(
            "objects",
            []
        ):


            if obj.get(
                "type"
            ) == obj_type:


                result.append(
                    obj
                )


        return {

            "type":
                obj_type,


            "count":
                len(result),


            "results":
                result

        }



    # =====================================================
    # SEMANTIC SEARCH
    # =====================================================

    def semantic_search(
        self,
        text
    ):


        results = []


        data = self.graph.export()



        for obj in data.get(
            "objects",
            []
        ):


            content = str(
                obj
            ).lower()


            if text in content:


                results.append(
                    obj
                )



        return {

            "query":
                text,


            "results":
                results,


            "confidence":
                0.8

        }



    # =====================================================
    # GRAPH TRACE
    # =====================================================

    def trace(
        self,
        object_id
    ):


        chain = []


        data = self.graph.export()


        current = object_id


        chain.append(
            current
        )


        while True:


            relation = next(

                (
                    r for r in data.get(
                        "relations",
                        []
                    )

                    if r["from"] == current

                ),

                None

            )


            if not relation:

                break



            current = relation["to"]


            chain.append(
                current
            )


        return chain



    # =====================================================
    # NEXT RESEARCH STEPS
    # =====================================================

    def next_steps(self):


        return {


            "current_phase":
                self.project.phase,


            "progress":
                self.project.progress,


            "recommended_next":

            [

                "Complete Semantic Query Engine",

                "Build Context Transfer Layer",

                "Enable Autonomous Research Agent"

            ]

        }



    # =====================================================
    # CONTEXT FOR LLM TRANSFER
    # =====================================================

    def build_context(self):


        return {


            "timestamp":
                datetime.datetime.utcnow().isoformat(),


            "project":
                self.project.to_dict(),


            "knowledge_graph":
                self.graph.export(),


            "summary":
                self.project.summary()

        }

