import pytest

from ..types import PackageReference


@pytest.mark.parametrize(
    "reference_string, should_raise",
    [
        ["someUser-SomePackage", False],
        ["someUser-SomePackage-1.0.2", False],
        ["some-user-that-has-dashes-SomePackage-1.0.6", False],
        ["some-user-that-has-dashes-SomePackage-1.2.23.2.23.0.6", True],
        ["someUser-SomePackage-1.2.3.2", True],
        ["someUser-1.2.3", True],
        ["someUser-", True],
        ["asd", True],
        ["some-user-with-dashers-SomePackage", False],
        ["239423-2fwjeoifjw32023", False],
        ["a-b", False],
        ["a-b-0.0.1", False],
        ["fjwieojfoi wejoiof w", True],
        ["someUser-somePackage-1231203912.43.249234234", False],
    ],
)
def test_type_parsing(reference_string, should_raise):
    if should_raise:
        with pytest.raises(ValueError):
            PackageReference.parse(reference_string)
    else:
        parsed = str(PackageReference.parse(reference_string))
        assert parsed == reference_string


def test_equals_another_type():
    A = PackageReference.parse("SomeAuthor-SomePackage-1.0.0")
    assert (A == 49) is False


@pytest.mark.parametrize(
    "A_str, B_str, assertion",
    [
        ["someUser-SomePackage", "someUser-SomePackage", True],
        ["someUser-SomePackage", "someUser-SomePackage-1.0.0", False],
        ["someUser-SomePackage-1.0.0", "someUser-SomePackage-1.0.0", True],
        [
            "someUser-SomePackage-112312.120931.242392",
            "someUser-SomePackage-112312.120931.242392",
            True,
        ],
        ["someUser-SomePackage-1.0.0", "someUser-SomePackage-1.0.1", False],
        ["someUser-AnotherPackage-1.0.0", "someUser-SomePackage-1.0.0", False],
        ["SomeUser-SomePackage-1.0.0", "someUser-SomePackage-1.0.0", False],
        ["someUser-SomePackage-1.0.0", "someUser-SomePackage-1.1.0", False],
        ["someUser-SomePackage-1.0.0", "someUser-SomePackage-2.0.0", False],
    ],
)
def test_is_same_version(A_str, B_str, assertion):
    A = PackageReference.parse(A_str)
    B = PackageReference.parse(B_str)
    assert (A == B) == assertion
    assert A.is_same_version(B) == assertion
    assert (str(A) == str(B)) == assertion
    assert str(A) == A_str
    assert str(B) == B_str


@pytest.mark.parametrize(
    "A_str, B_str, assertion",
    [
        ["someUser-SomePackage", "someUser-SomePackage", True],
        ["someUser-SomePackage", "someUser-SomePackage-1.0.0", True],
        ["someUser-SomePackage", "someUser-SomePackage-1.2.0", True],
        ["someUser-SomePackage", "someUser-SomePackage-1.2.4", True],
        ["someUser-SomePackage", "someUser-SomePackage-0.2.4", True],
        ["someUser-SomePackage", "someUser-SomePackages-0.2.4", False],
        ["someUser-SomePackages", "someUser-SomePackages-0.2.4", True],
        ["asd-SomePackages", "someUser-SomePackages-0.2.4", False],
        ["someUser-SomePackages-2.0.2", "someUser-SomePackages-0.2.4", True],
        ["someUser-SomePackages-423.0.2", "someUser-SomePackages-0.2.4", True],
    ],
)
def test_is_same_package(A_str, B_str, assertion):
    A = PackageReference.parse(A_str)
    B = PackageReference.parse(B_str)
    assert A.is_same_package(B) == assertion
    assert str(A) == A_str
    assert str(B) == B_str
