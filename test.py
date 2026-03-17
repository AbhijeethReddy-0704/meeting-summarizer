from summarizer import summarize_meeting
import json

sample = """
John: Alright everyone, let's get started. We need to decide on the
launch date for v2.0. Marketing wants end of March.

Sarah: Engineering can hit March 28th if we cut the analytics dashboard
from scope. That feature needs 2 more weeks minimum.

John: Let's cut it. March 28th it is. Sarah, can you update the roadmap?

Sarah: Sure, I'll do that by Friday.

John: Great. Mike, what's the status on the payment integration?

Mike: Still blocked on the Stripe API keys. I need those from DevOps.

John: I'll chase DevOps today. Let's wrap up.
"""

result = summarize_meeting(sample)
print(json.dumps(result, indent=2))