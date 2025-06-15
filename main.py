from dotenv import load_dotenv
from src.workflow import Workflow

load_dotenv("local.env")


def main():
    workflow = Workflow()
    print("Invention & IP Research Assistant")

    while True:
        query = input("\n Innovation Query: ").strip()
        if query.lower() in {"quit", "exit"}:
            break
        
        if query:
            result = workflow.run(query)
            print(f"\n Results for: {query}")
            print("=" * 60)

        for i, invention in enumerate(result.inventions, 1):
                print(f"\n{i}. {invention.name}")
                print(f"    Website: {invention.website}")
                print(f"    Domain: {invention.technical_domain}")
                print(f"    Maturity: {invention.maturity_level}")
                print(f"    Patent Activity: {invention.patent_activity}")

                if invention.novelty_features:
                    print(f"   🔍 Novel Features: {', '.join(invention.novelty_features[:5])}")

                if invention.implementation_details:
                    print(f"   ⚙️ Implementation: {', '.join(invention.implementation_details[:5])}")

                if invention.potential_applications:
                    print(f"   🌍 Applications: {', '.join(invention.potential_applications[:4])}")

                if invention.description and invention.description != "Failed":
                    print(f"   Summary: {invention.description}")

                if invention.ip_protection_notes:
                    print(f"   IP Notes: {invention.ip_protection_notes}")

                print()

        if result.analysis:
                print("Recommendations: ")
                print("-" * 40)
                print(result.analysis)


if __name__ == "__main__":
    main()