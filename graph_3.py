def find_path_recursive(current_value, path_library, visited_library, graph, printed_paths):
    if current_value not in visited_library:
        path_library.append(current_value)
        visited_library.add(current_value)

        if current_value in graph:
            for next_value in graph[current_value]:
                find_path_recursive(next_value, path_library, visited_library, graph, printed_paths)

        if current_value in root_library and tuple(path_library) not in printed_paths:
            print(" ".join(reversed(path_library)))
            printed_paths.add(tuple(path_library))

        if path_library:
            visited_library.remove(current_value)
            path_library.pop()


def main():
    Dictionary = {}
    library_way = []
    tender_library = input().strip().split(' ')
    global root_library
    root_library = input().strip().split(' ')

    for line in fileinput.input():
        items = line.strip().split(' ')
        lib = items[0]
        for value in items[1:]:
            Dictionary.setdefault(value, []).append(lib)

    printed_paths = set()
    for path_value in tender_library:
        find_path_recursive(path_value, library_way, set(), Dictionary, printed_paths)


if __name__ == "__main__":
    import fileinput
    main()
