import random
import logging
from transformers import pipeline

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class QuoteGenerator:
    """
    Generates marriage quotes using the transformers library.
    Falls back to a predefined list if there are any issues with the model.
    """

    def __init__(self):
        """Initialize the quote generator with transformers pipeline."""
        # Fallback quotes in case the model fails
        self.fallback_quotes = [
            "A successful marriage requires falling in love many times, always with the same person.",
            "Marriage is not just spiritual communion, it is also remembering to take out the trash.",
            "The secret of a happy marriage is finding the right person. You know they're right if you love being with them all the time.",
            "A great marriage is not when the 'perfect couple' comes together. It is when an imperfect couple learns to enjoy their differences.",
            "Marriage is like a garden. It takes time, effort, and patience to cultivate something beautiful.",
            "The first to apologize is the bravest. The first to forgive is the strongest. The first to forget is the happiest.",
            "Marriage is not about finding a person you can live with, it's about finding the person you can't live without.",
            "Love is patient, love is kind. It does not envy, it does not boast, it is not proud.",
            "A happy marriage is about three things: memories of togetherness, forgiveness of mistakes, and a promise to never give up on each other.",
            "The best thing to hold onto in life is each other.",
            "Marriage is a commitment to do what it takes to make the relationship work. It's a promise to love in good times and bad.",
            "In marriage, each partner is to be an encourager rather than a critic, a forgiver rather than a collector of hurts.",
            "Marriage is a thousand little things. It's giving up your right to be right in the heat of an argument.",
            "The greatest marriages are built on teamwork, mutual respect, a healthy dose of admiration, and a never-ending portion of love and grace.",
            "Marriage is not a noun; it's a verb. It isn't something you get. It's something you do. It's the way you love your partner every day.",
            "A long-lasting marriage is built on trust, respect, and forgiveness. It's about choosing to love each other even in those moments when you struggle to like each other.",
            "The beauty of marriage is not always seen from the beginning—but rather as love grows and develops over time.",
            "Marriage is a daily commitment to grow together, to work through every joy and pain together, and to love each other fully.",
            "A good marriage is one where each partner secretly suspects they got the better deal.",
            "Marriage is the highest form of teamwork, where two people become one without losing their individuality.",
            "The most important thing a father can do for his children is to love their mother.",
            "Marriage is a sacred bond that unites two souls in a covenant of love, trust, and mutual respect.",
            "In the arithmetic of love, one plus one equals everything, and two minus one equals nothing.",
            "A godly marriage is a reflection of God's love for His people—unconditional, sacrificial, and enduring.",
            "The strength of marriage lies in learning to share your life, and always putting the other person first."
        ]

        # Try to initialize the transformers pipeline
        try:
            logger.info("Initializing transformers pipeline...")
            self.generator = pipeline('text-generation', model='gpt2')
            logger.info("Transformers pipeline initialized successfully")
            self.use_model = True
        except Exception as e:
            logger.warning(f"Failed to initialize transformers pipeline: {str(e)}")
            logger.info("Falling back to predefined quotes")
            self.use_model = False

    def generate_quote(self):
        """
        Generate a marriage quote.

        Uses the transformers model if available, otherwise falls back to predefined quotes.
        """
        if self.use_model:
            try:
                prompt = "Provide a godly marriage quote:"
                result = self.generator(prompt, max_length=50, num_return_sequences=1)
                generated_text = result[0]['generated_text'].strip()

                # Clean up the generated text
                # Sometimes the model output includes the prompt, so we remove it
                if generated_text.startswith(prompt):
                    generated_text = generated_text[len(prompt):].strip()

                # If the generated text is too short or empty, use a fallback
                if len(generated_text) < 20:
                    return random.choice(self.fallback_quotes)

                return generated_text
            except Exception as e:
                logger.warning(f"Error generating quote with model: {str(e)}")
                return random.choice(self.fallback_quotes)
        else:
            return random.choice(self.fallback_quotes)
