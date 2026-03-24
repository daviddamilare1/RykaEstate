from django import template

register = template.Library()

@register.filter
def format_price(value):
    try:
        # Convert value to float for numeric operations
        value = float(value)
        if value >= 1_000_000 and value % 1_000_000 == 0:
            # Format as millions (e.g., 1000000 -> 1M)
            return f"{int(value / 1_000_000)}M"
        elif value >= 1_000_000:
            # Format as millions with decimals (e.g., 1500000 -> 1.5M)
            return f"{value / 1_000_000:.1f}M".rstrip('0').rstrip('.')
        elif value >= 1_000 and value % 1_000 == 0:
            # Format as thousands (e.g., 100000 -> 100K)
            return f"{int(value / 1_000)}K"
        elif value >= 1_000:
            # Format as thousands with decimals (e.g., 1500 -> 1.5K)
            return f"{value / 1_000:.1f}K".rstrip('0').rstrip('.')
        else:
            # Return as is if less than 1000
            return f"{int(value)}" if value.is_integer() else f"{value:.2f}"
    except (ValueError, TypeError):
        return value  # Return original value if conversion fails