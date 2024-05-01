import json

class Candidate:
    def __init__(self, name, party):
        self.name = name
        self.party = party
        self.votes = 0

    def add_vote(self):
        self.votes += 1

class Election:
    def __init__(self, title, counting_method, num_seats):
        self.title = title
        self.counting_method = counting_method
        self.num_seats = num_seats
        self.candidates = []

    def add_candidate(self, candidate):
        self.candidates.append(candidate)

    def conduct_election(self):
        print(f"Conducting {self.title} Election with {self.counting_method} counting method.")

        if self.counting_method == "Single non-transferable vote":
            self.single_non_transferable_vote()
        elif self.counting_method == "Preferential voting":
            self.preferential_voting()
        elif self.counting_method == "Party list proportional representation":
            self.party_list_proportional_representation()

    def single_non_transferable_vote(self):
        winner = max(self.candidates, key=lambda x: x.votes)
        print(f"The winner of the election is {winner.name} from {winner.party} with {winner.votes} votes.")

    def preferential_voting(self):
        while True:
            votes = [candidate.votes for candidate in self.candidates]
            total_votes = sum(votes)
            majority_threshold = total_votes / 2 + 1

            # Check for majority
            if max(votes) >= majority_threshold:
                winner = self.candidates[votes.index(max(votes))]
                print(f"The winner of the election is {winner.name} from {winner.party} with {winner.votes} votes.")
                break

            # Find candidate with fewest votes
            min_votes = min(votes)
            candidate_to_eliminate = self.candidates[votes.index(min_votes)]

            # Eliminate candidate
            self.candidates.remove(candidate_to_eliminate)

            # Redistribute votes
            for candidate in self.candidates:
                candidate.votes += candidate_to_eliminate.votes_by_candidate(candidate)

    def party_list_proportional_representation(self):
        total_votes = sum(candidate.votes for candidate in self.candidates)
        party_votes = {}

        # Calculate total votes for each party
        for candidate in self.candidates:
            if candidate.party not in party_votes:
                party_votes[candidate.party] = 0
            party_votes[candidate.party] += candidate.votes

        # Calculate seats for each party
        seats_per_party = {}
        for party, votes in party_votes.items():
            seats_per_party[party] = (votes / total_votes) * self.num_seats

        # Allocate seats to candidates of each party
        for candidate in self.candidates:
            candidate.seats = int(seats_per_party[candidate.party])

        # Sort candidates by votes
        sorted_candidates = sorted(self.candidates, key=lambda x: x.votes, reverse=True)

        # Assign seats to candidates
        for candidate in sorted_candidates:
            if candidate.seats > 0:
                print(f"{candidate.name} from {candidate.party} wins {candidate.seats} seats.")
                candidate.seats -= 1

    def display_results(self):
        print("\nElection Results:")
        for candidate in self.candidates:
            print(f"{candidate.name} ({candidate.party}): {candidate.votes} votes")

class ElectionSystem:
    def __init__(self):
        self.elections = []

    def add_election(self, election):
        self.elections.append(election)

    def delete_election(self, election_title):
        for election in self.elections:
            if election.title == election_title:
                self.elections.remove(election)
                print(f"Election '{election_title}' deleted.")
                return
        print("Election not found.")

    def save_data(self, filename):
        with open(filename, 'w') as file:
            data = {
                "elections": [
                    {
                        "title": election.title,
                        "counting_method": election.counting_method,
                        "num_seats": election.num_seats,
                        "candidates": [
                            {
                                "name": candidate.name,
                                "party": candidate.party,
                                "votes": candidate.votes
                            }
                            for candidate in election.candidates
                        ]
                    }
                    for election in self.elections
                ]
            }
            json.dump(data, file, indent=4)

    def load_data(self, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            for election_data in data["elections"]:
                election = Election(election_data["title"], election_data["counting_method"], election_data["num_seats"])
                for candidate_data in election_data["candidates"]:
                    candidate = Candidate(candidate_data["name"], candidate_data["party"])
                    candidate.votes = candidate_data["votes"]
                    election.add_candidate(candidate)
                self.elections.append(election)

if __name__ == "__main__":
    election_system = ElectionSystem()

    try:
        election_system.load_data("election_data.json")
        print("Data loaded successfully.")
    except FileNotFoundError:
        print("No existing data found.")

    while True:
        print("\nMenu:")
        print("[1] Create an election")
        print("[2] Edit an election")
        print("[3] Count an election")
        print("[4] Delete an election")
        print("[5] Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            title = input("Enter the title of the election: ")
            counting_method = input("Enter the counting method (1. Single non-transferable vote 2. Preferential voting 3. Party list proportional representation): ")
            num_seats = int(input("Enter the number of seats up for election: "))

            election = Election(title, counting_method, num_seats)
            election_system.add_election(election)
            print("Election created.")

        elif choice == "2":
            # Edit an election
            election_title = input("Enter the title of the election you want to edit: ")
            for election in election_system.elections:
                if election.title == election_title:
                    print(f"Editing election '{election.title}'")
                    print("\nEdit options:")
                    print("[1] Rename the election")
                    print("[2] Change the Electoral System")
                    print("[3] Add candidate")
                    print("[4] Remove candidate")
                    print("[5] Add vote")
                    print("[6] Remove vote")
                    print("[7] Back to main menu")

                    edit_choice = input("Enter your edit choice: ")

                    if edit_choice == "1":
                        new_title = input("Enter the new title: ")
                        election.title = new_title
                        print("Election title updated.")
                    elif edit_choice == "2":
                        new_counting_method = input("Enter the new counting method: ")
                        election.counting_method = new_counting_method
                        print("Counting method updated.")
                    elif edit_choice == "3":
                        candidate_name = input("Enter the name of the candidate: ")
                        candidate_party = input("Enter the party of the candidate: ")
                        candidate = Candidate(candidate_name, candidate_party)
                        election.add_candidate(candidate)
                        print("Candidate added.")
                    elif edit_choice == "4":
                        candidate_name = input("Enter the name of the candidate to remove: ")
                        for candidate in election.candidates:
                            if candidate.name == candidate_name:
                                election.candidates.remove(candidate)
                                print("Candidate removed.")
                                break
                        else:
                            print("Candidate not found.")
                    elif edit_choice == "5":
                        candidate_name = input("Enter the name of the candidate to add vote to: ")
                        for candidate in election.candidates:
                            if candidate.name == candidate_name:
                                candidate.add_vote()
                                print("Vote added.")
                                break
                        else:
                            print("Candidate not found.")
                    elif edit_choice == "6":
                        candidate_name = input("Enter the name of the candidate to remove vote from: ")
                        for candidate in election.candidates:
                            if candidate.name == candidate_name:
                                if candidate.votes > 0:
                                    candidate.votes -= 1
                                    print("Vote removed.")
                                else:
                                    print("No votes to remove.")
                                break
                        else:
                            print("Candidate not found.")
                    elif edit_choice == "7":
                        break
                    else:
                        print("Invalid choice.")
                    break
            else:
                print("Election not found.")

        elif choice == "3":
            # Count an election
            election_title = input("Enter the title of the election to count: ")
            for election in election_system.elections:
                if election.title == election_title:
                    election.conduct_election()
                    election.display_results()
                    break
            else:
                print("Election not found.")

        elif choice == "4":
            # Delete an election
            print("\nSelect an election to delete:")
            for i, election in enumerate(election_system.elections, start=1):
                print(f"[{i}] {election.title}")

            delete_choice = input("Enter the number of the election to delete (0 to cancel): ")
            if delete_choice.isdigit():
                delete_index = int(delete_choice) - 1
                if 0 <= delete_index < len(election_system.elections):
                    election_title = election_system.elections[delete_index].title
                    election_system.delete_election(election_title)
                elif delete_index == -1:
                    print("Operation canceled.")
                else:
                    print("Invalid choice.")
            else:
                print("Invalid input.")

        elif choice == "5":
            # Exit
            print("Exiting program. Saving data...")
            election_system.save_data("election_data.json")
            print("Data saved. Goodbye!")
            break

        else:
            print("Invalid choice.")