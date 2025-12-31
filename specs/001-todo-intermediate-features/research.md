# Research: Intermediate Level Features Implementation

## Architecture Research

### Models Layer
- **Task Entity**: Enhanced to include priority, tags, and creation timestamp
- **Validation**: Input validation for priority levels (high/medium/low) and tag format
- **Data Storage**: In-memory list/dict structure for efficient access

### Services Layer
- **TodoService**: Core business logic for task operations
  - Create, read, update, delete (CRUD) operations
  - Search functionality with keyword matching
  - Filter operations by status, priority, tags
  - Sort operations by priority, title, creation order
- **ValidationService**: Input validation and error handling

### CLI Layer
- **Main CLI**: Command parsing and routing
- **Command Handlers**: Individual handlers for each CLI command
- **Output Formatting**: Consistent display formatting for tasks with priorities and tags

## Best Practices for In-Memory CLI Task Management

### Performance Considerations
- For up to 1000 tasks, simple linear search/filter operations are acceptable
- Use list comprehensions for filtering operations
- Implement stable sort algorithms to preserve creation order when priorities are equal

### Deterministic Filter/Sort Logic
- Filters use AND logic when multiple criteria are specified
- Tags filter uses OR logic (task matches if it has ANY of the specified tags)
- Sort operations are stable to maintain consistent output

### User-Friendly Display Formatting
- Priority displayed as [HIGH], [MEDIUM], [LOW]
- Tags displayed as #work #home format
- Consistent formatting across all list operations

## Trade-offs Analysis

### Filtering Logic Options
- **AND vs OR for multiple filters**: AND logic chosen for precision (only tasks matching ALL criteria)
- **OR vs AND for tags**: OR logic chosen to allow flexible tag-based filtering (task matches if it has ANY of the specified tags)

### Data Structure Options
- **List vs Dict for storage**: List chosen for simplicity and natural ordering
- **Separate indexes**: Not implemented initially to maintain simplicity, may add if performance issues arise

### Sorting Implementation
- **Built-in sorted() vs custom sorting**: Built-in sorted() with key functions chosen for simplicity and performance
- **Stable sorting**: Used to maintain consistent output for equal priority items