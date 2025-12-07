"""Using the Registry class.

This example demonstrates how to use the Registry class
to register and instantiate objects dynamically.
"""

from __future__ import annotations

from objectory import Registry


# Create a registry instance
registry = Registry()


# Example 1: Register classes using decorator
@registry.register()
class EmailNotifier:
    """Send notifications via email."""

    def __init__(self, smtp_server: str = "localhost") -> None:
        """Initialize email notifier."""
        self.smtp_server = smtp_server

    def notify(self, message: str) -> str:
        """Send notification."""
        return f"Email via {self.smtp_server}: {message}"


@registry.register()
class SlackNotifier:
    """Send notifications via Slack."""

    def __init__(self, webhook_url: str = "https://hooks.slack.com/default") -> None:
        """Initialize Slack notifier."""
        self.webhook_url = webhook_url

    def notify(self, message: str) -> str:
        """Send notification."""
        return f"Slack to {self.webhook_url}: {message}"


# Example 2: Register classes in sub-registry
@registry.sms.register()
class TwilioSMSNotifier:
    """Send SMS via Twilio."""

    def __init__(self, account_sid: str = "default") -> None:
        """Initialize Twilio notifier."""
        self.account_sid = account_sid

    def notify(self, message: str) -> str:
        """Send notification."""
        return f"SMS via Twilio ({self.account_sid}): {message}"


@registry.sms.register()
class NexmoSMSNotifier:
    """Send SMS via Nexmo."""

    def notify(self, message: str) -> str:
        """Send notification."""
        return f"SMS via Nexmo: {message}"


# Example 3: Register with custom name
@registry.push.register("fcm")
class FirebaseNotifier:
    """Send push notifications via Firebase."""

    def notify(self, message: str) -> str:
        """Send notification."""
        return f"Push via Firebase: {message}"


def main() -> None:
    """Demonstrate Registry usage."""
    print("=" * 60)
    print("Registry Usage Examples")
    print("=" * 60)

    # Example 1: View registered objects
    print("\n1. Main registry objects:")
    for name in sorted(registry.registered_names()):
        print(f"   - {name}")

    # Example 2: View sub-registry objects
    print("\n2. SMS sub-registry objects:")
    for name in sorted(registry.sms.registered_names()):
        print(f"   - {name}")

    print("\n3. Push sub-registry objects:")
    for name in sorted(registry.push.registered_names()):
        print(f"   - {name}")

    # Example 4: Create objects from main registry
    print("\n4. Creating EmailNotifier:")
    notifier = registry.factory(_target_="EmailNotifier", smtp_server="smtp.example.com")
    print(f"   {notifier.notify('Hello from Email!')}")

    # Example 5: Create objects from sub-registry
    print("\n5. Creating TwilioSMSNotifier:")
    notifier = registry.sms.factory(_target_="TwilioSMSNotifier", account_sid="AC123456")
    print(f"   {notifier.notify('Hello from SMS!')}")

    # Example 6: Create with custom name
    print("\n6. Creating Firebase notifier using custom name:")
    notifier = registry.push.factory(_target_="fcm")
    print(f"   {notifier.notify('Hello from Push!')}")

    # Example 7: Using short names
    print("\n7. Using short class names:")
    notifier = registry.factory(_target_="SlackNotifier")
    print(f"   {notifier.notify('Hello from Slack!')}")

    # Example 8: Register object manually
    print("\n8. Manually registering a class:")

    class WebhookNotifier:
        """Send notifications via webhook."""

        def __init__(self, url: str) -> None:
            """Initialize webhook notifier."""
            self.url = url

        def notify(self, message: str) -> str:
            """Send notification."""
            return f"Webhook to {self.url}: {message}"

    registry.webhook.register_object(WebhookNotifier)
    notifier = registry.webhook.factory(
        _target_="WebhookNotifier", url="https://example.com/webhook"
    )
    print(f"   {notifier.notify('Hello from Webhook!')}")

    # Example 9: Clear a sub-registry
    print("\n9. Clearing webhook sub-registry:")
    print(f"   Before: {registry.webhook.registered_names()}")
    registry.webhook.clear()
    print(f"   After:  {registry.webhook.registered_names()}")

    print("\n" + "=" * 60)
    print("All examples completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
