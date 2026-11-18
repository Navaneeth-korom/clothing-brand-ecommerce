from google import genai
from google.genai import types
from django.conf import settings
from .exceptions import ChatbotServiceError
import logging
from google.genai import errors

logger = logging.getLogger(__name__)

def generate_reply(message):
    try:
        client = genai.Client(
            api_key= settings.GEMINI_API_KEY
        )

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents= message,
            config=types.GenerateContentConfig(
                system_instruction= (
                    "You are LUMINA's official AI customer support assistant for an online clothing store. "
                    "Help customers with product information, clothing recommendations, sizes, orders, "
                    "payments, shipping, returns, and general shopping questions. "
                    "Maintain a friendly, professional, and helpful tone. "
                    "Keep answers concise, ideally within 3 short sentences. "
                    "Never invent product details, prices, stock availability, order status, or store policies. "
                    "If you don't have the required information, politely say so and guide the customer "
                    "to contact LUMINA's support team."
                )
            )
            
        )
        reply = response.text

        if not reply or not reply.strip():
            raise ChatbotServiceError(
                "I couldn't generate a response. Please try again.",
                status_code=502
            )

        return reply

    except ChatbotServiceError:
        raise

    except errors.APIError as e:
        logger.error(
            "Gemini API error: status=%s, message=%s",
            e.code,
            e.message
        )

        if e.code == 429:
            raise ChatbotServiceError(
                "Our assistant is temporarily busy. Please try again later.",
                status_code=503
            )

        elif e.code == 503:
            raise ChatbotServiceError(
                "Our assistant is temporarily unavailable. Please try again.",
                status_code=503
            )

        elif e.code == 504:
            raise ChatbotServiceError(
                "The request took too long. Please try again.",
                status_code=504
            )

        elif e.code in (401, 403):
            raise ChatbotServiceError(
                "Our assistant is currently unavailable.",
                status_code=503
            )

        else:
            raise ChatbotServiceError(
                "Something went wrong. Please try again.",
                status_code=502
            )

    except Exception:
        logger.exception("Unexpected chatbot service error")

        raise ChatbotServiceError(
            "Unable to connect to our assistant. Please try again.",
            status_code=502
        )