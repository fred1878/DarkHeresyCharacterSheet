from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

# -----------------------------
# Fundamental data structures
# -----------------------------

@dataclass
class AttributeBlock:
    """Represents the nine standard Dark Heresy characteristics."""

    ws: int = 0  # Weapon Skill
    bs: int = 0  # Ballistic Skill
    s: int = 0   # Strength
    t: int = 0   # Toughness
    ag: int = 0  # Agility
    int_: int = 0  # Intelligence (``int`` is a keyword)
    per: int = 0  # Perception
    wp: int = 0   # Willpower
    fel: int = 0  # Fellowship

    def as_dict(self) -> Dict[str, int]:
        """Return a dict representation suitable for ``ConfigParser``."""
        return {
            "WS": self.ws,
            "BS": self.bs,
            "S": self.s,
            "T": self.t,
            "Ag": self.ag,
            "Int": self.int_,
            "Per": self.per,
            "WP": self.wp,
            "Fel": self.fel,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, str | int]) -> "AttributeBlock":
        return cls(
            ws=int(data.get("WS", 0)),
            bs=int(data.get("BS", 0)),
            s=int(data.get("S", 0)),
            t=int(data.get("T", 0)),
            ag=int(data.get("Ag", 0)),
            int_=int(data.get("Int", 0)),
            per=int(data.get("Per", 0)),
            wp=int(data.get("WP", 0)),
            fel=int(data.get("Fel", 0)),
        )


@dataclass
class Skill:
    trained: bool = False
    rank: int = 0

    def as_tuple(self) -> tuple[str, str]:
        return ("yes" if self.trained else "no", str(self.rank))

    @classmethod
    def from_tuple(cls, tup: tuple[str, str]) -> "Skill":
        trained_str, rank_str = tup
        return cls(trained=trained_str.lower() in {"yes", "true", "1"}, rank=int(rank_str))


# A non-exhaustive default list of Dark Heresy skills; users can extend it later.
DEFAULT_SKILLS = [
    "Acrobatics",
    "Awareness",
    "Barter",
    "Carouse",
    "Charm",
    "Climb",
    "Command",
    "Common Lore",
    "Concealment",
    "Contortionist",
    "Deceive",
    "Disguise",
    "Dodge",
    "Drive",
    "Evaluate",
    "Forbidden Lore",
    "Gamble",
    "Inquiry",
    "Interrogation",
    "Intimidate",
    "Logic",
    "Medicae",
    "Navigate",
    "Operate",
    "Parry",
    "Pilot",
    "Psyniscience",
    "Scholastic Lore",
    "Scrutiny",
    "Search",
    "Security",
    "Silent Move",
    "Speak Language",
    "Survival",
    "Swim",
    "Tech-Use",
    "Tracking",
    "Trade",
]


@dataclass
class Character:
    # ------------------- Basic Info --------------------
    name: str = ""
    homeworld: str = ""
    background: str = ""
    role: str = ""
    divination: str = ""
    gender: str = ""
    height: str = ""
    weight: str = ""
    age: str = ""
    build: str = ""
    hair: str = ""
    eyes: str = ""
    aura: str = ""

    # ------------------- Statistics --------------------
    attributes: AttributeBlock = field(default_factory=AttributeBlock)

    # Skills: mapping skill name → Skill object
    skills: Dict[str, Skill] = field(
        default_factory=lambda: {name: Skill() for name in DEFAULT_SKILLS}
    )

    # TODO: Add wounds, talents, equipment, etc.

    # ----------------------------------------------------
    def as_config(self) -> "configparser.ConfigParser":
        import configparser

        cfg = configparser.ConfigParser()

        # Basic section
        cfg["Basic"] = {
            "Name": self.name,
            "Homeworld": self.homeworld,
            "Background": self.background,
            "Role": self.role,
            "Divination": self.divination,
            "Gender": self.gender,
            "Height": self.height,
            "Weight": self.weight,
            "Age": self.age,
            "Build": self.build,
            "Hair": self.hair,
            "Eyes": self.eyes,
            "Aura": self.aura,
        }

        # Attributes
        cfg["Attributes"] = {k: str(v) for k, v in self.attributes.as_dict().items()}

        # Skills
        skills_section: Dict[str, str] = {}
        for name, skill in self.skills.items():
            trained_str, rank_str = skill.as_tuple()
            skills_section[f"{name}_Trained"] = trained_str
            skills_section[f"{name}_Rank"] = rank_str
        cfg["Skills"] = skills_section

        return cfg

    @classmethod
    def from_config(cls, cfg: "configparser.ConfigParser") -> "Character":
        # Basic section may not exist in malformed files – use get with fallback.
        basic = cfg["Basic"] if "Basic" in cfg else {}
        attributes = cfg["Attributes"] if "Attributes" in cfg else {}
        skills_section = cfg["Skills"] if "Skills" in cfg else {}

        char = cls(
            name=basic.get("Name", ""),
            homeworld=basic.get("Homeworld", ""),
            background=basic.get("Background", ""),
            role=basic.get("Role", ""),
            divination=basic.get("Divination", ""),
            gender=basic.get("Gender", ""),
            height=basic.get("Height", ""),
            weight=basic.get("Weight", ""),
            age=basic.get("Age", ""),
            build=basic.get("Build", ""),
            hair=basic.get("Hair", ""),
            eyes=basic.get("Eyes", ""),
            aura=basic.get("Aura", ""),
            attributes=AttributeBlock.from_dict(attributes),
        )

        # Parse skills
        for name in DEFAULT_SKILLS:
            trained_key = f"{name}_Trained"
            rank_key = f"{name}_Rank"
            trained = skills_section.get(trained_key, "no")
            rank = skills_section.get(rank_key, "0")
            char.skills[name] = Skill.from_tuple((trained, rank))

        return char