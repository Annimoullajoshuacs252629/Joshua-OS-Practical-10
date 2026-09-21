import random

# ==================== GLOBAL FILE SYSTEM DATA ====================
MAX_FILES = 10
TOTAL_BLOCKS = 32
BLOCK_SIZE = 64

disk = [0] * TOTAL_BLOCKS  # 0 = Free, 1 = Allocated
directory = []  # Stores dictionary elements for files


# ==================== PART 1: DISK SCHEDULING ====================

def fcfs(req, head):
    seek_count = 0
    curr_head = head
    seq = [curr_head]
    
    for track in req:
        seek_count += abs(track - curr_head)
        curr_head = track
        seq.append(curr_head)
        
    print("\n--- FCFS Disk Scheduling ---")
    print("Seek Sequence:", " -> ".join(map(str, seq)))
    print(f"Total Seek Operations: {seek_count}")


def sstf(req, head):
    seek_count = 0
    curr_head = head
    seq = [curr_head]
    requests = req.copy()
    
    while requests:
        nearest = min(requests, key=lambda x: abs(x - curr_head))
        seek_count += abs(nearest - curr_head)
        curr_head = nearest
        seq.append(curr_head)
        requests.remove(nearest)
        
    print("\n--- SSTF Disk Scheduling ---")
    print("Seek Sequence:", " -> ".join(map(str, seq)))
    print(f"Total Seek Operations: {seek_count}")


def c_scan(req, head, disk_size=200):
    seek_count = 0
    curr_head = head
    arr = sorted(req + [0, disk_size - 1])
    
    pos = 0
    for i, track in enumerate(arr):
        if track >= curr_head:
            pos = i
            break
            
    seq = [curr_head]
    
    # Head moves right
    for track in arr[pos:]:
        seek_count += abs(track - curr_head)
        curr_head = track
        seq.append(curr_head)
        
    # Jump to 0
    seek_count += abs((disk_size - 1) - 0)
    curr_head = 0
    
    # Head moves right again up to pos
    for track in arr[:pos]:
        if track == 0:
            continue
        seek_count += abs(track - curr_head)
        curr_head = track
        seq.append(curr_head)
        
    print("\n--- C-SCAN Disk Scheduling ---")
    print("Seek Sequence:", " -> ".join(map(str, seq)))
    print(f"Total Seek Operations: {seek_count}")


def c_look(req, head):
    seek_count = 0
    curr_head = head
    arr = sorted(req)
    
    pos = 0
    for i, track in enumerate(arr):
        if track >= curr_head:
            pos = i
            break
            
    seq = [curr_head]
    
    # Right direction
    for track in arr[pos:]:
        seek_count += abs(track - curr_head)
        curr_head = track
        seq.append(curr_head)
        
    # Wrap around to start of array
    for track in arr[:pos]:
        seek_count += abs(track - curr_head)
        curr_head = track
        seq.append(curr_head)
        
    print("\n--- C-LOOK Disk Scheduling ---")
    print("Seek Sequence:", " -> ".join(map(str, seq)))
    print(f"Total Seek Operations: {seek_count}")


def rss(req, head):
    seek_count = 0
    curr_head = head
    seq = [curr_head]
    shuffled_req = req.copy()
    random.shuffle(shuffled_req)
    
    for track in shuffled_req:
        seek_count += abs(track - curr_head)
        curr_head = track
        seq.append(curr_head)
        
    print("\n--- RSS (Random Scheduling System) ---")
    print("Seek Sequence:", " -> ".join(map(str, seq)))
    print(f"Total Seek Operations: {seek_count}")


def run_disk_scheduling():
    req = [98, 183, 37, 122, 14, 124, 65, 67]
    head = 53
    disk_size = 200

    print("\nDisk Requests:", req)
    print(f"Initial Head Position: {head}")

    fcfs(req, head)
    sstf(req, head)
    c_scan(req, head, disk_size)
    c_look(req, head)
    rss(req, head)


# ==================== PART 2: FILE SYSTEM DESIGN ====================

def create_file():
    if len(directory) >= MAX_FILES:
        print("\nError: Directory full!")
        return

    name = input("Enter File Name: ").strip()
    content = input("Enter File Content: ")

    blocks_needed = max(1, (len(content) + BLOCK_SIZE - 1) // BLOCK_SIZE)

    start = -1
    free_count = 0
    for i in range(TOTAL_BLOCKS):
        if disk[i] == 0:
            if free_count == 0:
                start = i
            free_count += 1
            if free_count == blocks_needed:
                break
        else:
            free_count = 0
            start = -1

    if free_count < blocks_needed:
        print("\nError: Not enough contiguous disk space!")
        return

    for i in range(start, start + blocks_needed):
        disk[i] = 1

    file_entry = {
        "name": name,
        "start_block": start,
        "length": blocks_needed,
        "data": content
    }
    directory.append(file_entry)

    print(f"\nFile '{name}' created! Allocated blocks: {start} to {start + blocks_needed - 1}")


def read_file():
    name = input("Enter File Name to Read: ").strip()
    for f in directory:
        if f["name"] == name:
            print(f"\n--- Reading File '{name}' ---")
            print(f"Content: {f['data']}")
            print(f"Blocks Used: {f['length']} (Start Block: {f['start_block']})")
            return
    print(f"\nError: File '{name}' not found!")


def delete_file():
    name = input("Enter File Name to Delete: ").strip()
    for f in directory:
        if f["name"] == name:
            for i in range(f["start_block"], f["start_block"] + f["length"]):
                disk[i] = 0
            directory.remove(f)
            print(f"\nFile '{name}' deleted successfully!")
            return
    print(f"\nError: File '{name}' not found!")


def display_directory():
    print("\n================ DIRECTORY ================")
    if not directory:
        print("Directory is empty.")
        return
    print(f"{'File Name':<15} {'Start Block':<15} {'Block Count':<10}")
    print("-" * 43)
    for f in directory:
        print(f"{f['name']:<15} {f['start_block']:<15} {f['length']:<10}")


# ==================== MAIN MENU ====================

def main():
    while True:
        print("\n=============================================")
        print("            OS PRACTICAL NO. 10              ")
        print("Name: Joshua | Roll No: S072")
        print("=============================================")
        print("1. Run Disk Scheduling Simulations (FCFS, SSTF, C-SCAN, C-LOOK, RSS)")
        print("2. File System Operations (Create, Read, Delete, Directory)")
        print("3. Exit")
        
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            run_disk_scheduling()
        elif choice == '2':
            while True:
                print("\n--- File System Operations ---")
                print("1. Create File\n2. Read File\n3. Delete File\n4. Display Directory\n5. Back to Main Menu")
                fs_choice = input("Choice: ").strip()
                if fs_choice == '1':
                    create_file()
                elif fs_choice == '2':
                    read_file()
                elif fs_choice == '3':
                    delete_file()
                elif fs_choice == '4':
                    display_directory()
                elif fs_choice == '5':
                    break
                else:
                    print("Invalid choice!")
        elif choice == '3':
            print("Exiting Program.")
            break
        else:
            print("Invalid option! Try again.")

if __name__ == "__main__":
    main()
