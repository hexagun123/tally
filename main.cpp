#include <iostream>
#include <fstream>
#include "json.hpp"

using json = nlohmann::json;

using namespace std;

// Function to print out everything in the JSON object in a more organized way
void updatejson(const json &j) {
    cout << "Subjects:\n";
    for (auto& [subject, grades] : j["subjects"].items()) {
        cout << "  " << subject << ":\n";
        cout << "    Expected: " << grades["expected"] << "\n";
        cout << "    Current: " << grades["current"] << "\n";
    }

    cout << "\nExtra Curriculars:\n";
    for (auto& [activity, details] : j["extra_curriculars"].items()) {
        cout << "  " << activity << ":\n";
        cout << "    Streak: " << details["Streak"] << "\n";
        cout << "    Updated: " << (details["Updated"] ? "Yes" : "No") << "\n";
    }

    cout << "\nLast Opened: " << j["last_opened"] << "\n";
}

// Function to handle user input and update the JSON object
void userinput(json &j) {
    // Ask user for choices on what to change
    cout << "What would you like to change?\n";
    cout << "1. Subjects\n";
    cout << "2. Extra Curriculars\n";
    cout << "3. Print out everything\n";
    cout << "Enter your choice: ";
    int choice;
    cin >> choice;

    switch (choice) {
        case 1:
            // Handle subjects update
            cout << "Create new subjects (Y/N)";
            char option;
            cin >> option;
            if (option == 'Y' || option == 'y') {
                // Create new subject
                cout << "Enter the new subject: ";
                string new_subject;
                cin.ignore();
                getline(cin, new_subject);
                cout << "Enter the expected grade for " << new_subject << ": ";
                string new_grade;
                cin.ignore();
                cin >> new_grade;
                j["subjects"][new_subject]["expected"] = new_grade;
                cout << "Enter the current grade for " << new_subject << ": ";
                cin >> new_grade;
                j["subjects"][new_subject]["current"] = new_grade;
            } else if (option == 'N' || option == 'n') {
                // Print out all the subjects
                cout << "Current subjects:\n";
                for (auto& [key, value] : j["subjects"].items()) {
                    cout << "\t" << key << ": " << value << "\n";
                }

                // Update existing subject
                cout << "Enter the subject you want to update: (n for return)";
                string subject;
                cin >> subject;
                if (subject == "n") {
                    break;
                }
                if (j["subjects"].contains(subject)) {
                    cout << "Enter the current grade for " << subject << ": ";
                    string new_grade;
                    cin >> new_grade;
                    j["subjects"][subject]["current"] = new_grade;
                } else {
                    cout << "Invalid subject.\n";
                }
            } else {
                cout << "Invalid option. Please enter Y or N.\n";
            }
            break;
        case 2:
            // Handle extra curriculars update
            cout << "Do you want to create new activity (Y/N): ";
            char create_option;
            cin >> create_option;
            if (create_option == 'Y' || create_option == 'y') {
                // Create new activity
                cout << "Enter the new activity: ";
                string new_activity;
                cin.ignore();
                getline(cin, new_activity);
                j["extra_curriculars"][new_activity] = {{"Updated", false}, {"Streak", 0}};
            } else if (create_option == 'N' || create_option == 'n') {
                // Update existing activity
                cout << "Choose one of the activities below that you did:\n";
                for (auto& [key, value] : j["extra_curriculars"].items()) {
                    cout << key << " (Streak: " << value["Streak"] << ", Updated: " << value["Updated"] << ")\n";
                }
                cout << "Enter the activity you want to update: (press n to force quit)";
                string activity;
                cin >> activity;
                if (j["extra_curriculars"].contains(activity)) {
                    if (!j["extra_curriculars"][activity]["Updated"]) {
                        j["extra_curriculars"][activity]["Updated"] = true;
                        j["extra_curriculars"][activity]["Streak"] = j["extra_curriculars"][activity]["Streak"].get<int>() + 1;
                    } else {
                        cout << "Activity already updated.\n";
                    }
                } else {
                    cout << "Invalid activity.\n";
                }
            } else {
                cout << "Invalid option. Please enter Y or N.\n";
            }
            break;
        case 3:
            // Print out the JSON object
            updatejson(j);
            break;
        default:
            cout << "Invalid choice.\n";
            return;
    }

    // Update the last opened date to the current date automatically
    time_t now = time(0);
    tm *ltm = localtime(&now);
    j["last_opened"] = to_string(1900 + ltm->tm_year) + "-" + 
                       to_string(1 + ltm->tm_mon) + "-" + 
                       to_string(ltm->tm_mday);

    // Save the updated JSON to a file
    ofstream file("status.json");
    file << j.dump(4);
    file.close();
}

int main() {
    // Create a JSON object
    json j;

    // Try to open the existing status.json file
    ifstream file("status.json");
    if (file.is_open()) {
        // If the file exists, parse the JSON data
        file >> j;
        file.close();
    } else {
        // If the file does not exist, initialize the JSON structure
        j["subjects"] = json::object(); // Subjects with grades
        j["extra_curriculars"] = json::object(); // Extra curricular activities with streaks
        j["last_opened"] = "2023-10-05"; // Last opened date
    }
    // Check if the last opened date matches the current date
    time_t now = time(0);
    tm *ltm = localtime(&now);
    string current_date = to_string(1900 + ltm->tm_year) + "-" + 
                          to_string(1 + ltm->tm_mon) + "-" + 
                          to_string(ltm->tm_mday);

    if (j["last_opened"] != current_date) {
        // Loop through all the extracurriculars
        for (auto& [key, value] : j["extra_curriculars"].items()) {
            if (!value["Updated"]) {
                value["Streak"] = 0;
            }
            value["Updated"] = false;
        }
    }
    // Loop to allow multiple updates
    while (true) {
        userinput(j);
        cout << "Do you want to make another change? (y/n): ";
        char cont;
        cin >> cont;
        if (cont == 'n' || cont == 'N') {
            break;
        }
    }

    return 0;
}