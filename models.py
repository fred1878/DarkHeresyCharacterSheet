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
class WoundsBlock:
    current: int = 0
    max: int = 0
    fatigue: int = 0

    def as_dict(self) -> Dict[str, int]:
        return {"Current": self.current, "Max": self.max, "Fatigue": self.fatigue}

    @classmethod
    def from_dict(cls, data: Dict[str, str | int]) -> "WoundsBlock":
        return cls(
            current=int(data.get("Current", 0)),
            max=int(data.get("Max", 0)),
            fatigue=int(data.get("Fatigue", 0)),
        )


@dataclass
class MovementBlock:
    half: int = 0
    full: int = 0
    charge: int = 0
    run: int = 0

    def as_dict(self) -> Dict[str, int]:
        return {
            "Half": self.half,
            "Full": self.full,
            "Charge": self.charge,
            "Run": self.run,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, str | int]) -> "MovementBlock":
        return cls(
            half=int(data.get("Half", 0)),
            full=int(data.get("Full", 0)),
            charge=int(data.get("Charge", 0)),
            run=int(data.get("Run", 0)),
        )


@dataclass
class ExperienceBlock:
    total: int = 0
    spent: int = 0

    @property
    def remaining(self) -> int:
        return max(0, self.total - self.spent)

    def as_dict(self) -> Dict[str, int]:
        return {"Total": self.total, "Spent": self.spent, "Remaining": self.remaining}

    @classmethod
    def from_dict(cls, data: Dict[str, str | int]) -> "ExperienceBlock":
        return cls(total=int(data.get("Total", 0)), spent=int(data.get("Spent", 0)))


@dataclass
class ArmourBlock:
    head: int = 0
    arms: int = 0
    body: int = 0
    legs: int = 0

    def as_dict(self) -> Dict[str, int]:
        return {
            "Head": self.head,
            "Arms": self.arms,
            "Body": self.body,
            "Legs": self.legs,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, str | int]) -> "ArmourBlock":
        return cls(
            head=int(data.get("Head", 0)),
            arms=int(data.get("Arms", 0)),
            body=int(data.get("Body", 0)),
            legs=int(data.get("Legs", 0)),
        )


@dataclass
class Weapon:
    name: str = ""
    wtype: str = ""  # e.g., Melee, Ranged
    wclass: str = ""  # e.g., Basic, Pistol
    range: str = ""  # could be "30m" or "–" for melee
    rof: str = ""  # Rate of Fire string e.g., "S/2/–"
    damage: str = ""  # e.g., "1d10+4 R"
    penetration: int = 0
    clip: str = ""  # e.g., "30"
    reload: str = ""  # e.g., "Full"
    special: str = ""  # free-text qualities

    _DELIM = " | "

    def to_string(self) -> str:
        parts = [
            self.name,
            self.wtype,
            self.wclass,
            self.range,
            self.rof,
            self.damage,
            str(self.penetration),
            self.clip,
            self.reload,
            self.special,
        ]
        return self._DELIM.join(parts)

    @classmethod
    def from_string(cls, s: str) -> "Weapon":
        parts = s.split(cls._DELIM)
        # Pad missing fields
        parts += [""] * (10 - len(parts))
        return cls(
            name=parts[0].strip(),
            wtype=parts[1].strip(),
            wclass=parts[2].strip(),
            range=parts[3].strip(),
            rof=parts[4].strip(),
            damage=parts[5].strip(),
            penetration=int(parts[6].strip() or 0),
            clip=parts[7].strip(),
            reload=parts[8].strip(),
            special=parts[9].strip(),
        )


# Psychic power simple representation
@dataclass
class PsychicPower:
    name: str = ""

    def to_string(self) -> str:
        return self.name

    @classmethod
    def from_string(cls, s: str) -> "PsychicPower":
        return cls(name=s.strip())


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

    # ------------------- Combat & Misc -----------------
    wounds: WoundsBlock = field(default_factory=WoundsBlock)
    movement: MovementBlock = field(default_factory=MovementBlock)

    # Lists stored as simple strings for now
    talents: List[str] = field(default_factory=list)
    gear: List[str] = field(default_factory=list)

    # Combat equipment & powers
    armour: ArmourBlock = field(default_factory=ArmourBlock)
    weapons: List[Weapon] = field(default_factory=list)

    psy_rating: int = 0
    psychic_powers: List[PsychicPower] = field(default_factory=list)

    # Mental status & afflictions
    corruption: int = 0
    insanity: int = 0
    mutations: List[str] = field(default_factory=list)
    disorders: List[str] = field(default_factory=list)

    experience: ExperienceBlock = field(default_factory=ExperienceBlock)

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

        # Wounds & Movement
        cfg["Wounds"] = {k: str(v) for k, v in self.wounds.as_dict().items()}
        cfg["Movement"] = {k: str(v) for k, v in self.movement.as_dict().items()}

        # Experience
        cfg["Experience"] = {k: str(v) for k, v in self.experience.as_dict().items()}

        # Armour, Weapons, Psychic Powers & Status
        cfg["Armour"] = {k: str(v) for k, v in self.armour.as_dict().items()}

        cfg["Weapons"] = {
            "Items": "\n".join(w.to_string() for w in self.weapons)
        }

        cfg["Psyker"] = {
            "Rating": str(self.psy_rating),
            "Powers": "\n".join(p.to_string() for p in self.psychic_powers),
        }

        cfg["CorruptionInsanity"] = {
            "Corruption": str(self.corruption),
            "Insanity": str(self.insanity),
        }

        cfg["Mutations"] = {"Items": "\n".join(self.mutations)}
        cfg["Disorders"] = {"Items": "\n".join(self.disorders)}

        # Talents & Gear (store as newline‐separated list in single key)
        cfg["Talents"] = {"Items": "\n".join(self.talents)}
        cfg["Gear"] = {"Items": "\n".join(self.gear)}

        return cfg

    @classmethod
    def from_config(cls, cfg: "configparser.ConfigParser") -> "Character":
        # Basic section may not exist in malformed files – use get with fallback.
        basic = cfg["Basic"] if "Basic" in cfg else {}
        attributes = cfg["Attributes"] if "Attributes" in cfg else {}
        skills_section = cfg["Skills"] if "Skills" in cfg else {}
        wounds_section = cfg["Wounds"] if "Wounds" in cfg else {}
        movement_section = cfg["Movement"] if "Movement" in cfg else {}
        xp_section = cfg["Experience"] if "Experience" in cfg else {}
        talents_section = cfg["Talents"] if "Talents" in cfg else {}
        gear_section = cfg["Gear"] if "Gear" in cfg else {}
        armour_section = cfg["Armour"] if "Armour" in cfg else {}
        weapons_section = cfg["Weapons"] if "Weapons" in cfg else {}
        psy_section = cfg["Psyker"] if "Psyker" in cfg else {}
        corruption_section = cfg["CorruptionInsanity"] if "CorruptionInsanity" in cfg else {}
        mutations_section = cfg["Mutations"] if "Mutations" in cfg else {}
        disorders_section = cfg["Disorders"] if "Disorders" in cfg else {}

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
            wounds=WoundsBlock.from_dict(wounds_section),
            movement=MovementBlock.from_dict(movement_section),
            experience=ExperienceBlock.from_dict(xp_section),
            armour=ArmourBlock.from_dict(armour_section),
        )

        # Parse skills
        for name in DEFAULT_SKILLS:
            trained_key = f"{name}_Trained"
            rank_key = f"{name}_Rank"
            trained = skills_section.get(trained_key, "no")
            rank = skills_section.get(rank_key, "0")
            char.skills[name] = Skill.from_tuple((trained, rank))

        # Talents / Gear
        talents_items = talents_section.get("Items", "").splitlines()
        char.talents = [t for t in talents_items if t.strip()]

        gear_items = gear_section.get("Items", "").splitlines()
        char.gear = [g for g in gear_items if g.strip()]

        # Weapons list
        weapon_lines = weapons_section.get("Items", "").splitlines()
        char.weapons = [Weapon.from_string(line) for line in weapon_lines if line.strip()]

        # Psyker
        char.psy_rating = int(psy_section.get("Rating", 0))
        power_lines = psy_section.get("Powers", "").splitlines()
        char.psychic_powers = [PsychicPower.from_string(l) for l in power_lines if l.strip()]

        # Corruption/Insanity
        char.corruption = int(corruption_section.get("Corruption", 0))
        char.insanity = int(corruption_section.get("Insanity", 0))

        # Mutations / Disorders
        char.mutations = [m for m in mutations_section.get("Items", "").splitlines() if m.strip()]
        char.disorders = [d for d in disorders_section.get("Items", "").splitlines() if d.strip()]

        return char