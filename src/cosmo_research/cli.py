import argparse
import json

from .assumption_auditor import AssumptionAuditor
from .config import Settings
from .literature.ads import ADSClient
from .literature.arxiv import ArxivIngestor
from .literature.index import LiteratureIndex
from .llm.deepseek import DeepSeekClient


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cosmo-research")
    sub = parser.add_subparsers(dest="command", required=True)

    ingest = sub.add_parser("ingest", help="Retrieve and index literature")
    ingest.add_argument("query")
    ingest.add_argument("--ads", action="store_true", help="Include NASA ADS")
    ingest.add_argument("--arxiv", action="store_true", help="Include arXiv")
    ingest.add_argument("--rows", type=int, default=50)

    search = sub.add_parser("search", help="Search the literature index")
    search.add_argument("query")
    search.add_argument("--limit", type=int, default=10)

    audit = sub.add_parser("audit", help="Audit text assumptions")
    audit.add_argument("file", help="UTF-8 text or Markdown file")

    reason = sub.add_parser("reason", help="Send a prompt to DeepSeek-R1")
    reason.add_argument("prompt")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    settings = Settings()

    if args.command == "ingest":
        if not args.ads and not args.arxiv:
            args.arxiv = True
        papers = []
        if args.ads:
            if not settings.ads_api_token:
                raise SystemExit("Set ADS_API_TOKEN to use the ADS client")
            papers.extend(ADSClient(settings.ads_api_token).search(args.query, args.rows))
        if args.arxiv:
            papers.extend(ArxivIngestor().search(args.query, args.rows))
        index = LiteratureIndex(settings.chroma_persist_dir, settings.chroma_collection)
        print(json.dumps({"retrieved": len(papers), "indexed": index.index(papers), "total_in_index": index.count}))

    elif args.command == "search":
        index = LiteratureIndex(settings.chroma_persist_dir, settings.chroma_collection)
        print(json.dumps(index.search(args.query, args.limit), default=str, indent=2))

    elif args.command == "audit":
        with open(args.file, "r", encoding="utf-8") as audit_file:
            text = audit_file.read()
        print(json.dumps(AssumptionAuditor().audit_report(text), indent=2))

    elif args.command == "reason":
        if not settings.deepseek_api_key:
            raise SystemExit("Set DEEPSEEK_API_KEY to use DeepSeek-R1")
        client = DeepSeekClient(settings.deepseek_api_key, settings.deepseek_base_url, settings.deepseek_model)
        print(client.reason(args.prompt))


if __name__ == "__main__":
    main()
