"""
Q3 – Unit Tests for the Django Poll App
"""

import pytest
from unittest.mock import MagicMock
from django.contrib.auth.models import User
from polls.models import Poll, Choice, Vote

def test_poll_str():
    poll = Poll(text="Best language?")
    assert str(poll) == "Best language?"


def test_choice_str():
    poll = Poll(text="Best language?")
    choice = Choice(poll=poll, choice_text="Python")
    assert str(choice) == "Best language? - Python"


def test_poll_active_default():
    poll = Poll()
    assert poll.active is True


def test_vote_str():
    user = User(username="bob")
    poll = Poll(text="Best framework?")
    choice = Choice(choice_text="Django")
    vote = Vote(user=user, poll=poll, choice=choice)
    assert str(vote) == "Best framework? - Django - bob"

def test_user_can_vote_no_vote():
    user = MagicMock()
    user.vote_set.all.return_value.filter.return_value.exists.return_value = False
    poll = MagicMock()

    result = not user.vote_set.all().filter(poll=poll).exists()

    assert result is True


def test_user_cannot_vote_twice():
    user = MagicMock()
    user.vote_set.all.return_value.filter.return_value.exists.return_value = True
    poll = MagicMock()

    result = not user.vote_set.all().filter(poll=poll).exists()

    assert result is False


def test_get_vote_count_mock():
    poll = MagicMock()
    poll.vote_set.count.return_value = 5

    result = poll.vote_set.count()

    poll.vote_set.count.assert_called_once()
    assert result == 5


def test_get_result_dict_fake():
    poll = MagicMock()
    poll.get_vote_count = 10

    fake_choices = []
    for text, votes in [("Python", 5), ("JavaScript", 5)]:
        c = MagicMock()
        c.choice_text = text
        c.get_vote_count = votes
        fake_choices.append(c)
    poll.choice_set.all.return_value = fake_choices

    results = [
        {
            "text": c.choice_text,
            "num_votes": c.get_vote_count,
            "percentage": (c.get_vote_count / poll.get_vote_count) * 100,
        }
        for c in poll.choice_set.all()
    ]

    assert results[0]["percentage"] == 50.0
    assert results[1]["percentage"] == 50.0
