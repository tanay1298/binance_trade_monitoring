# Database Design Documentation

## Table Name: Trade

### Table Description:
The Trade table stores information about individual trades in the cryptocurrency market. Each record in the Trade table represents a single trade event involving the buying or selling of a particular cryptocurrency asset.

### Table Fields:

- **event_type**:
  - Data Type: CharField (max_length=100)
  - Description: Represents the type of event, such as 'trade'.
  
- **event_time**:
  - Data Type: BigIntegerField
  - Description: Represents the timestamp of the trade event, indicating when the trade occurred.
  
- **symbol**:
  - Data Type: CharField (max_length=100)
  - Description: Represents the symbol or identifier of the cryptocurrency asset involved in the trade.
  
- **trade_id**:
  - Data Type: BigIntegerField
  - Description: Unique identifier for the trade event.
  
- **price**:
  - Data Type: DecimalField (max_digits=20, decimal_places=8)
  - Description: Represents the price at which the trade occurred.
  
- **quantity**:
  - Data Type: DecimalField (max_digits=20, decimal_places=8)
  - Description: Represents the quantity of the cryptocurrency asset traded.
  
- **buy_order_id**:
  - Data Type: BigIntegerField
  - Description: Identifier for the buy order associated with the trade.
  
- **sell_order_id**:
  - Data Type: BigIntegerField
  - Description: Identifier for the sell order associated with the trade.
  
- **trade_completed_time**:
  - Data Type: BigIntegerField
  - Description: Represents the timestamp when the trade was completed.
  
- **is_maker**:
  - Data Type: BooleanField
  - Description: Indicates whether the trade was initiated by a maker.
  
- **is_taker**:
  - Data Type: BooleanField
  - Description: Indicates whether the trade was initiated by a taker.
  
- **created_at**:
  - Data Type: DateTimeField (auto_now_add=True)
  - Description: Represents the timestamp when the record was created in the database.

### Database Table Constraints:

No explicit constraints defined in the provided model. Additional constraints such as primary keys, unique constraints, or foreign key relationships may be implemented based on specific requirements.

### Database Indexes:

No explicit indexes defined in the provided model. Indexes may be added to optimize query performance based on frequently accessed fields or search patterns.

### Normalization:

The provided Trade table appears to be in first normal form (1NF) as each field contains atomic values, and there are no repeating groups. Further normalization considerations depend on the specific requirements of the application and the relationships between tables in the database schema.

### Design Choices:

- The use of BigIntegerField for fields such as trade_id, event_time, trade_completed_time allows for the storage of large integer values, accommodating timestamps and unique identifiers commonly encountered in cryptocurrency trading.
- DecimalField with appropriate precision (max_digits=20, decimal_places=8) is used for fields representing numeric values such as price and quantity, ensuring accuracy in financial calculations.
- BooleanField is used for fields is_maker and is_taker to represent binary true/false values indicating the maker/taker status of the trade event.
- The auto_now_add=True parameter in the created_at field ensures that the field is automatically populated with the current timestamp when a new record is inserted into the table.

### Future Considerations:

- As the application evolves, additional fields, constraints, or indexes may be introduced to accommodate new requirements or improve database performance.
- Regular monitoring and optimization of database queries may be necessary to maintain optimal performance, especially as the volume of trade data increases over time.

This document provides an overview of the Trade table's schema, including field definitions, constraints, design choices, and considerations for future enhancements.
