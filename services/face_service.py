import cv2
import numpy as np
import insightface
from PIL import Image


class FaceService:

    def __init__(self):

        self.model = insightface.app.FaceAnalysis(
            providers=["CPUExecutionProvider"]
        )

        self.model.prepare(ctx_id=0)

    def _prepare_image(self, image):

        if isinstance(image, Image.Image):
            image = np.array(image)

        # RGB -> BGR
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        return image

    def _select_document_face(self, faces):

        if not faces:
            return None

        def face_area(face):

            x1, y1, x2, y2 = face.bbox

            return (x2 - x1) * (y2 - y1)

        # Largest detected face first
        faces = sorted(
            faces,
            key=face_area,
            reverse=True
        )

        return faces[0]

    def verify(self, document_image, selfie_image):

        # ---------------------------------
        # Prepare images
        # ---------------------------------

        document_image = self._prepare_image(document_image)
        selfie_image = self._prepare_image(selfie_image)

        # ---------------------------------
        # Detect faces
        # ---------------------------------

        face_doc = self.model.get(document_image)
        face_selfie = self.model.get(selfie_image)

        # ---------------------------------
        # Document face check
        # ---------------------------------

        if len(face_doc) == 0:

            return {
                "status": "FAILED",
                "reason": "No face found in document.",
                "matched": False
            }

        # ---------------------------------
        # Selfie face check
        # ---------------------------------

        if len(face_selfie) == 0:

            return {
                "status": "FAILED",
                "reason": "No face found in selfie.",
                "matched": False
            }

        # ---------------------------------
        # Multiple face protection
        # ---------------------------------

        
        if len(face_selfie) > 1:

            return {
                "status": "FAILED",
                "reason": "Multiple faces found in selfie.",
                "matched": False
            }

        # ---------------------------------
        # Get embeddings
        # ---------------------------------

        document_face = self._select_document_face(face_doc)

        if document_face is None:

            return {
                "status": "FAILED",
                "reason": "Unable to select face from document.",
                "matched": False
            }

        selfie_embedding = face_selfie[0].embedding

        face_similarities = []

        for i, document_face in enumerate(face_doc):

            document_embedding = document_face.embedding

            similarity = np.dot(
                document_embedding,
                selfie_embedding
            ) / (
                np.linalg.norm(document_embedding) *
                np.linalg.norm(selfie_embedding)
            )

            face_similarities.append({
                "face_index": i,
                "similarity": round(float(similarity), 3)
            })

        # Select the highest similarity only for analysis
        best_match = max(
            face_similarities,
            key=lambda x: x["similarity"]
        )

        similarity = best_match["similarity"]

        similarity = float(similarity)

        # ---------------------------------
        # Matching threshold
        # ---------------------------------

        threshold = 0.55

        matched = similarity >= threshold

        # ---------------------------------
        # Result
        # ---------------------------------

        return {
            "status": "SUCCESS",

            "similarity": similarity,

            "threshold": threshold,

            "document_faces_detected": len(face_doc),

            "selfie_faces_detected": len(face_selfie),

            "face_similarities": face_similarities,

            "best_face_index": best_match["face_index"],

            "matched": matched,

            "reason": (
                "Face matched successfully."
                if matched
                else "Face does not match the document."
            )
        }