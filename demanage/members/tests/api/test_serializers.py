"""
Serializers are responsible for:

- convering data models (only specific fields) to primitive types (dict)
- rendering primitive types in JSON
- validating data when creating/updating instance
"""
import pytest

from demanage.members.api.serializers import MemberSerializer
from demanage.members.models import Member
from demanage.members.tests.factories import MemberFactory

pytestmark = pytest.mark.django_db


def test_serialize_member_object(member: Member):
    """Test object is serialized to dict correctly.
    Valid fields and data are serailized.
    """
    serializer = MemberSerializer(member)
    assert serializer.data["username"] == member.user.username
    assert "join_time" in serializer.data


def test_serialize_member_object_list(member_factory: MemberFactory):
    MemberFactory()
    MemberFactory()
    MemberFactory()

    members = Member.objects.all()  # queryset is ordered by join time (ascending)
    serializer = MemberSerializer(instance=members, many=True)

    assert len(serializer.data) == 3
    assert serializer.data[0]["username"] == members[0].user.username
    assert "join_time" in serializer.data[0]
