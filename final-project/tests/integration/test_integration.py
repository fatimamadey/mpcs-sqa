import pytest
from django.contrib.auth.models import User
from django.urls import reverse

@pytest.fixture
def authenticated_client(db, client):
    """
    Create a real User in the test DB and return a logged-in test client.
    Uses pytest-django's `db` fixture so the test DB is set up.
    """
    user = User.objects.create_user(
        username="integrationuser",
        password="testpassword123",
        email="integration@test.com",
    )
    client.login(username="integrationuser", password="testpassword123")
    return client, user


# Test 1 – View ↔ Database
def test_polls_list_view_returns_polls_from_database(authenticated_client):
    """
    Integration test: polls_list view ↔ Poll database table.

    Creates real Poll rows in the test database, then hits the view
    through Django's test client and asserts the response contains
    the correct poll text — verifying the view queries the DB correctly.

    Components integrated: polls_list view (views.py) ↔ Poll model (models.py / DB)
    What could go wrong:
      - View might filter out polls (e.g., wrong queryset scope).
      - Paginator misconfiguration could hide rows on page 1.
      - A broken DB migration would cause OperationalError.
    """
    from polls.models import Poll

    client, user = authenticated_client

    # Arrange: insert two real polls directly into the test database
    poll_a = Poll.objects.create(owner=user, text="Integration Poll Alpha")
    poll_b = Poll.objects.create(owner=user, text="Integration Poll Beta")

    # Act: GET /polls/list/
    url = reverse("polls:list")
    response = client.get(url)

    # Assert: HTTP 200 and both poll texts appear in the rendered HTML
    assert response.status_code == 200
    content = response.content.decode()
    assert "Integration Poll Alpha" in content, "Poll A missing from response"
    assert "Integration Poll Beta" in content, "Poll B missing from response"


# Test 2 – View ↔ Template
def test_polls_list_view_renders_correct_template_with_context(authenticated_client):
    """
    Integration test: polls_list view ↔ polls/polls_list.html template.

    Asserts that the view:
      1. Renders the correct template.
      2. Passes the expected context variables ('polls', 'search_term').
      3. The template successfully renders without raising TemplateDoesNotExist.

    Components integrated: polls_list view (views.py) ↔ polls/polls_list.html
    What could go wrong:
      - A renamed context key breaks the template loop (e.g., 'polls' → 'poll_list').
      - A missing template file raises TemplateDoesNotExist and 500s.
      - 'search_term' missing from context means search UI renders broken.
    """
    from polls.models import Poll

    client, user = authenticated_client

    # Arrange: one poll so the template has something to iterate over
    Poll.objects.create(owner=user, text="Template Integration Poll")

    # Act: GET with a search term to exercise the search_term context variable
    url = reverse("polls:list")
    response = client.get(url, {"search": "Template"})

    # Assert 1: successful response
    assert response.status_code == 200

    # Assert 2: correct template used
    template_names = [t.name for t in response.templates]
    assert "polls/polls_list.html" in template_names, (
        f"Expected polls/polls_list.html, got: {template_names}"
    )

    # Assert 3: context variables are present
    assert "polls" in response.context, "'polls' key missing from context"
    assert "search_term" in response.context, "'search_term' key missing from context"
    assert response.context["search_term"] == "Template"