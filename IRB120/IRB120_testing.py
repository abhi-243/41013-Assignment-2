from IRB120 import IRB120
from IRB120Tester import IRB120Tester

def main():
    robot = IRB120()
    tester = IRB120Tester(robot)
    tester.initialize(use_swift=True)

    while True:
        print("\n-----------------------------------------")
        print("Select test mode:")
        print("1. Run trajectory test (all joints move together)")
        print("2. Test one joint")
        print("3. Test all joints")
        print("4. Run IK + trajectory test (pick & place)")
        print("5. Exit")
        print("-----------------------------------------")

        choice = input("Select (1/2/3/4/5): ").strip()

        if choice == "1":
            tester.trajectory_test()

        elif choice == "2":
            j = int(input("Enter joint number (1–6): ")) - 1
            tester.joint_test(joint_index=j)

        elif choice == "3":
            tester.joint_test(joint_index=None)

        elif choice == "4":
            print("\nSelect IK trajectory type:")
            print("  a) jtraj  – Joint-space interpolation (default)")
            print("  b) ctraj  – Cartesian linear motion")
            print("  c) mstraj – Multi-segment lift and place")
            sub = input("Choose (a/b/c): ").strip().lower()

            if sub == "a":
                tester.ik_trajectory_test(method="jtraj")
            elif sub == "b":
                tester.ik_trajectory_test(method="ctraj")
            elif sub == "c":
                tester.ik_trajectory_test(method="mstraj")
            else:
                print("Invalid choice, running default jtraj test.")
                tester.ik_trajectory_test(method="jtraj")

        elif choice == "5":
            print("Exiting program.")
            break

        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()