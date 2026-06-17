from datetime import datetime, timezone


PROJECT_NAME = "TZPID Proof Pipeline"
CREATOR_NAME = "Daniel Alexander Trawin"
CREATOR_ORCID = "0009-0001-4630-3715"
CREATOR_ORCID_URL = f"https://orcid.org/{CREATOR_ORCID}"


def generated_utc():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def provenance_dict(generator, sources=None, generated_at_utc=None, note=None):
    return {
        "project": PROJECT_NAME,
        "creator": CREATOR_NAME,
        "creator_orcid": CREATOR_ORCID,
        "creator_orcid_url": CREATOR_ORCID_URL,
        "generator": generator,
        "generated_at_utc": generated_at_utc or generated_utc(),
        "sources": sources or [],
        "note": note or "Generated proof-pipeline artifact; verify source hashes before treating as authoritative.",
    }


def plain_lines(generator, sources=None, generated_at_utc=None, note=None):
    provenance = provenance_dict(generator, sources, generated_at_utc, note)
    lines = [
        f"Project: {provenance['project']}",
        f"Creator: {provenance['creator']}",
        f"ORCID: {provenance['creator_orcid_url']}",
        f"Generator: {provenance['generator']}",
        f"Generated UTC: {provenance['generated_at_utc']}",
    ]
    if provenance["sources"]:
        lines.append("Sources:")
        lines.extend(f"- {source}" for source in provenance["sources"])
    lines.append(f"Note: {provenance['note']}")
    return lines


def isabelle_text(generator, sources=None, generated_at_utc=None, note=None):
    body = "\n  ".join(plain_lines(generator, sources, generated_at_utc, note))
    return f"text \\<open>\n  {body}\n\\<close>\n"


def wolfram_comment(generator, sources=None, generated_at_utc=None, note=None):
    body = "\n".join("  " + line for line in plain_lines(generator, sources, generated_at_utc, note))
    return f"(*\n{body}\n*)\n"


def lean_comment(generator, sources=None, generated_at_utc=None, note=None):
    body = "\n".join(plain_lines(generator, sources, generated_at_utc, note))
    return f"/-\n{body}\n-/"


def rocq_comment(generator, sources=None, generated_at_utc=None, note=None):
    body = "\n".join(plain_lines(generator, sources, generated_at_utc, note))
    return f"(*\n{body}\n*)"
