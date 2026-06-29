
def calculate_content_score(content: str) -> dict:
    """Calculates a simple deterministic content score for a given social media post."""
    if not content:
        return {
            "overall_score": 1,
            "hook_strength": 1,
            "readability": 1,
            "engagement": 1,
            "platform_fit": 1,
            "goal_alignment": 1,
        }

    lines = [line.strip() for line in content.split("\n") if line.strip()]
    first_line = lines[0] if lines else ""
    words = content.split()
    word_count = len(words)

    # 1. Hook Strength
    hook_strength = 4
    emojis = ["🚀", "🔥", "✨", "💡", "📢", "👋"]
    if any(emoji in first_line for emoji in emojis):
        hook_strength += 3
    if len(first_line) <= 80:
        hook_strength += 3
    if first_line.endswith("!") or first_line.endswith("?"):
        hook_strength += 2
    hook_strength = min(10, max(1, hook_strength))

    # 2. Readability
    readability = 1
    if 50 <= word_count <= 300:
        readability += 4
    if "\n" in content:
        readability += 3
    if lines and (word_count / len(lines)) <= 15:
        readability += 2
    readability = min(10, max(1, readability))

    # 3. Engagement
    engagement = 1
    if "?" in content:
        engagement += 4
    cta_words = ["comment below","feedback", "share", "thoughts","join", "agree", "disagree", "help", "let me know", "cta","subscribe","follow"]
    if any(w in content.lower() for w in cta_words):
        engagement += 3
    if any(emoji in content for emoji in emojis):
        engagement += 2
    if "#" in content:
        engagement += 1
    if len(lines) >= 4:
        engagement += 1
    engagement = min(10, max(1, engagement))

    # 4. Platform Fit
    platform_fit = 2
    if "#" in content:
        platform_fit += 1

    if "\n" in content:
        platform_fit += 3

    if any(emoji in content for emoji in emojis):
        platform_fit += 2

    platform_fit += 2
    platform_fit = min(10, max(1, platform_fit))

    # 5. Goal Alignment
    goal_alignment = 2
    if len(content) > 50:
        goal_alignment += 5
    if "?" in content or any(w in content.lower() for w in cta_words):
        goal_alignment += 3
    goal_alignment = min(10, max(1, goal_alignment))


    # Calculate overall_score from averages
    total = hook_strength + readability + engagement + platform_fit + goal_alignment
    overall_score = round((total / 50) * 100)

    if overall_score >= 80:
        grade = "Excellent"

    elif overall_score >= 60:
        grade = "Good"

    else:
        grade = "Needs Improvement"
    

    return {
        "overall_score": overall_score,
        "grade": grade,
        "hook_strength": hook_strength,
        "readability": readability,
        "engagement": engagement,
        "platform_fit": platform_fit,
        "goal_alignment": goal_alignment,
        
    }
