title: "A Warning For EF Core's DateTimeOffsetToBinaryConverter"
date: 2021-04-06
category: General
tags: [c#, ef-core, sqlite, database]
feature: feature.png
description: "I recently had some troubles sorting and filtering a DateTimeOffsetToBinaryConverter column in a SQLite database using ef-core. This looks into my issue, why it was happening and my solution."

[TOC]

## Summary

While starting a new .NET 5 project with Entity Framework Code, I tried creating a column of type DateTimeOffset in my SQLite database (expecting it to be translated by ef-core automatically). SQLite does not have support for DateTimeOffset let alone DateTimes and ef-core does not automatically map to something else, so I had to investigate other methods of storage.

DateTimes automatically map to INTEGER (stores ticks I believe), but I have heard they lose their `Kind` when coming back out of the database. This could be a good idea but I didn't want to call `.DateTime` everywhere.

[This post](https://blog.dangl.me/archive/handling-datetimeoffset-in-sqlite-with-entity-framework-core/) showed that we can use ef-core's [DateTimeOffsetToBinaryConverter](https://github.com/dotnet/efcore/blob/main/src/EFCore/Storage/ValueConversion/DateTimeOffsetToBinaryConverter.cs) converter to map a DateTimeOffset to a long which would then be mapped to an INTEGER (64bit) in SQLite.
 
Adding this in was very easy, but after a few months I realised some filters on these fields were a bit weird and sometimes the ordering was off.
 

## The Usage of DateTimeOffsetToBinaryConverter

This is how I had used DateTimeOffsetToBinaryConverter in my project:

Context.cs

```csharp
using Microsoft.EntityFrameworkCore;
using Server.Api.Database.Models;

namespace Server.Api.Database
{
    public class Context : DbContext
    {
        // Models ...

        public Context() : base() { }
        public Context(DbContextOptions<Context> options) : base(options) { }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.SetupContext(this.Database.IsSqlite()); // Identify if we are using a SQLite database
        }
    }
}

```

ContextSetup.cs

```csharp
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Storage.ValueConversion;
using Server.Api.Database.Models;
using System;
using System.Linq;

namespace Server.Api.Database
{
    public static class ContextSetup
    {
        public static void SetupContext(this ModelBuilder modelBuilder, bool isSQLite)
        {
            // Model building ...

            // Handle datetimes in SQLite src: https://blog.dangl.me/archive/handling-datetimeoffset-in-sqlite-with-entity-framework-core/
            if (isSQLite) // We found this in Context.cs
            {
                // SQLite does not have proper support for DateTimeOffset via Entity Framework Core, see the limitations
                // here: https://docs.microsoft.com/en-us/ef/core/providers/sqlite/limitations#query-limitations
                // To work around this, when the Sqlite database provider is used, all model properties of type DateTimeOffset
                // use the DateTimeOffsetToBinaryConverter
                // Based on: https://github.com/aspnet/EntityFrameworkCore/issues/10784#issuecomment-415769754
                // This only supports millisecond precision, but should be sufficient for most use cases.
                foreach (var entityType in modelBuilder.Model.GetEntityTypes())
                {
                    var properties = entityType.ClrType.GetProperties().Where(p => p.PropertyType == typeof(DateTimeOffset)
                                                                                || p.PropertyType == typeof(DateTimeOffset?));
                    foreach (var property in properties)
                    {
                        modelBuilder
                            .Entity(entityType.Name)
                            .Property(property.Name)
                            .HasConversion(new DateTimeOffsetToBinaryConverter()); // The converter!
                    }
                }
            }
        }
    }
}
```

## The Potential Issue

This looks cool and all - and it will work too. However, when we get times with different timezones, this seems to start creating a mess.

I first noticed this when my times were being stored in the database as +1300 (my timezone at the time) and I was filtering with a UTC DateTimeOffset. I had noticed that times in +1300 were being dropped off the end of my filter even though they had the same time as the end date (the query was inclusive).

I wrote a couple of tests to look at what I was seeing.

### Same Timezones Sort Well

```csharp
[TestMethod]
public void SameTimeZones_SortWell()
{
    // Create an instance of our converter and get some functions to map from DateTimeOffset to long and back (to simulate database storage)
    var converter = new DateTimeOffsetToBinaryConverter();
    var codeToDatabase = converter.ConvertToProviderExpression.Compile();
    var databaseToCode = converter.ConvertFromProviderExpression.Compile();

    // Our dates in their expected order
    var dateTimeOffsets = new List<DateTimeOffset>
    {
        new DateTimeOffset(2021, 3, 30, 11, 13, 59, new TimeSpan(0, 0, 0)),
        new DateTimeOffset(2021, 3, 30, 11, 14, 0, new TimeSpan(0, 0, 0)),
        new DateTimeOffset(2021, 3, 30, 11, 14, 1, new TimeSpan(0, 0, 0)),
        new DateTimeOffset(2021, 3, 30, 11, 14, 2, new TimeSpan(0, 0, 0)),
        new DateTimeOffset(2021, 3, 30, 11, 14, 3, new TimeSpan(0, 0, 0)),
        new DateTimeOffset(2021, 3, 30, 11, 14, 4, new TimeSpan(0, 0, 0)),
        new DateTimeOffset(2021, 3, 30, 11, 14, 5, new TimeSpan(0, 0, 0)),
    };

    // Shuffle the offsets for testing (external function)
    var dateTimeOffsetsShuffled = Shuffle(dateTimeOffsets);

    // Make them to the database representation
    var dateTimeOffsetsMappedToDatabase = dateTimeOffsetsShuffled
        .Select(x => codeToDatabase(x))
        .ToList();

    // Sort them
    var dateTimeOffsetsMappedToDatabaseOrdered = dateTimeOffsetsMappedToDatabase
        .OrderBy(x => x)
        .ToList();

    // Convert them back to DateTimeOffset objects
    var dateTimeOffsetsMappedBackToCode = dateTimeOffsetsMappedToDatabaseOrdered
        .Select(x => databaseToCode(x))
        .ToList();

    // Validate the list we now have matches the original input list
    for (var i = 0; i < dateTimeOffsets.Count; i++)
    {
        var difference = dateTimeOffsets[i] - dateTimeOffsetsMappedBackToCode[i];
        Assert.AreEqual(0, difference.TotalMilliseconds);
    }
}
```

This passes - as expected.

### Same Timezones Filter Well

```csharp
[TestMethod]
public void SameTimeZones_FilterWell()
{
    // Same as above
    var converter = new DateTimeOffsetToBinaryConverter();
    var codeToDatabase = converter.ConvertToProviderExpression.Compile();
    var databaseToCode = converter.ConvertFromProviderExpression.Compile();

    // Our input times in order
    var dateTimeOffsets = new List<DateTimeOffset>
    {
        new DateTimeOffset(2021, 3, 30, 11, 13, 59, new TimeSpan(0, 0, 0)),
        new DateTimeOffset(2021, 3, 30, 11, 14, 0, new TimeSpan(0, 0, 0)),
        new DateTimeOffset(2021, 3, 30, 11, 14, 1, new TimeSpan(0, 0, 0)),
        new DateTimeOffset(2021, 3, 30, 11, 14, 2, new TimeSpan(0, 0, 0)), // First item in filter
        new DateTimeOffset(2021, 3, 30, 11, 14, 3, new TimeSpan(0, 0, 0)),
        new DateTimeOffset(2021, 3, 30, 11, 14, 4, new TimeSpan(0, 0, 0)),
        new DateTimeOffset(2021, 3, 30, 11, 14, 5, new TimeSpan(0, 0, 0)),
        new DateTimeOffset(2021, 3, 30, 11, 14, 6, new TimeSpan(0, 0, 0)), // Last item in filter
        new DateTimeOffset(2021, 3, 30, 11, 14, 7, new TimeSpan(0, 0, 0)),
        new DateTimeOffset(2021, 3, 30, 11, 14, 8, new TimeSpan(0, 0, 0)),
    };
    // The times we will be filtering on (inclusive)
    var startTime = codeToDatabase(new DateTimeOffset(2021, 3, 30, 11, 14, 2, new TimeSpan(0, 0, 0)));
    var endTime = codeToDatabase(new DateTimeOffset(2021, 3, 30, 11, 14, 6, new TimeSpan(0, 0, 0)));
    // What we expect to see
    var dateTimeOffsetsFilteredExpectations = new List<DateTimeOffset>
    {
        new DateTimeOffset(2021, 3, 30, 11, 14, 2, new TimeSpan(0, 0, 0)), // First item in filter
        new DateTimeOffset(2021, 3, 30, 11, 14, 3, new TimeSpan(0, 0, 0)),
        new DateTimeOffset(2021, 3, 30, 11, 14, 4, new TimeSpan(0, 0, 0)),
        new DateTimeOffset(2021, 3, 30, 11, 14, 5, new TimeSpan(0, 0, 0)),
        new DateTimeOffset(2021, 3, 30, 11, 14, 6, new TimeSpan(0, 0, 0)), // Last item in filter
    };

    var dateTimeOffsetsMappedToDatabase = dateTimeOffsets
        .Select(x => codeToDatabase(x))
        .ToList();

    var dateTimeOffsetsMappedToDatabaseFiltered = dateTimeOffsetsMappedToDatabase
        .Where(x => x >= startTime)
        .Where(x => x <= endTime);

    var dateTimeOffsetsMappedBackToCode = dateTimeOffsetsMappedToDatabaseFiltered
        .Select(x => databaseToCode(x))
        .ToList();

    for (var i = 0; i < dateTimeOffsetsMappedBackToCode.Count; i++)
    {
        var difference = dateTimeOffsetsMappedBackToCode[i] - dateTimeOffsetsFilteredExpectations[i];
        Assert.AreEqual(0, difference.TotalMilliseconds);
    }
}
```

This passes - as expected.

### Different Timezones Don't Sort Well

```csharp
[TestMethod]
public void DifferentTimeZones_DoNotSortWell()
{
    var converter = new DateTimeOffsetToBinaryConverter();
    var codeToDatabase = converter.ConvertToProviderExpression.Compile();
    var databaseToCode = converter.ConvertFromProviderExpression.Compile();

    var dateTimeOffsets = new List<DateTimeOffset>
    {
        new DateTimeOffset(2021, 3, 30, 11, 13, 59, new TimeSpan(0, 0, 0)),
        new DateTimeOffset(2021, 3, 30, 11, 14, 0, new TimeSpan(0, 0, 0)),
        new DateTimeOffset(2021, 3, 30, 11, 14, 1, new TimeSpan(0, 0, 0)).ToOffset(new TimeSpan(13, 0, 0)),
        new DateTimeOffset(2021, 3, 30, 11, 14, 2, new TimeSpan(0, 0, 0)),
        new DateTimeOffset(2021, 3, 30, 11, 14, 3, new TimeSpan(0, 0, 0)),
        new DateTimeOffset(2021, 3, 30, 11, 14, 4, new TimeSpan(0, 0, 0)).ToOffset(new TimeSpan(13, 0, 0)),
        new DateTimeOffset(2021, 3, 30, 11, 14, 5, new TimeSpan(0, 0, 0)),
    };

    var dateTimeOffsetsShuffled = Shuffle(dateTimeOffsets);

    var dateTimeOffsetsMappedToDatabase = dateTimeOffsetsShuffled
        .Select(x => codeToDatabase(x))
        .ToList();

    var dateTimeOffsetsMappedToDatabaseOrdered = dateTimeOffsetsMappedToDatabase
        .OrderBy(x => x)
        .ToList();

    var dateTimeOffsetsMappedBackToCode = dateTimeOffsetsMappedToDatabaseOrdered
        .Select(x => databaseToCode(x))
        .ToList();

    for (var i = 0; i < dateTimeOffsets.Count; i++)
    {
        var difference = dateTimeOffsets[i] - dateTimeOffsetsMappedBackToCode[i];
        Assert.AreEqual(0, difference.TotalMilliseconds);
    }
}
```

This fails. Same data just with some DateTimeOffset objects converted to different timezones.

### Different Timezones Don't Filter Well

```csharp
[TestMethod]
public void DifferentTimeZones_DoNotFilterWell()
{
    var converter = new DateTimeOffsetToBinaryConverter();
    var codeToDatabase = converter.ConvertToProviderExpression.Compile();
    var databaseToCode = converter.ConvertFromProviderExpression.Compile();

    var dateTimeOffsets = new List<DateTimeOffset>
    {
        new DateTimeOffset(2021, 3, 30, 11, 13, 59, new TimeSpan(0, 0, 0)),
        new DateTimeOffset(2021, 3, 30, 11, 14, 0, new TimeSpan(0, 0, 0)),
        new DateTimeOffset(2021, 3, 30, 11, 14, 1, new TimeSpan(0, 0, 0)).ToOffset(new TimeSpan(13, 0, 0)),
        new DateTimeOffset(2021, 3, 30, 11, 14, 2, new TimeSpan(0, 0, 0)), // First item in filter
        new DateTimeOffset(2021, 3, 30, 11, 14, 3, new TimeSpan(0, 0, 0)).ToOffset(new TimeSpan(13, 0, 0)),
        new DateTimeOffset(2021, 3, 30, 11, 14, 4, new TimeSpan(0, 0, 0)),
        new DateTimeOffset(2021, 3, 30, 11, 14, 5, new TimeSpan(0, 0, 0)).ToOffset(new TimeSpan(13, 0, 0)),
        new DateTimeOffset(2021, 3, 30, 11, 14, 6, new TimeSpan(0, 0, 0)), // Last item in filter
        new DateTimeOffset(2021, 3, 30, 11, 14, 7, new TimeSpan(0, 0, 0)),
        new DateTimeOffset(2021, 3, 30, 11, 14, 8, new TimeSpan(0, 0, 0)),
    };
    var startTime = codeToDatabase(new DateTimeOffset(2021, 3, 30, 11, 14, 2, new TimeSpan(0, 0, 0)));
    var endTime = codeToDatabase(new DateTimeOffset(2021, 3, 30, 11, 14, 6, new TimeSpan(0, 0, 0)));
    var dateTimeOffsetsFilteredExpectations = new List<DateTimeOffset>
    {
        new DateTimeOffset(2021, 3, 30, 11, 14, 2, new TimeSpan(0, 0, 0)), // First item in filter
        new DateTimeOffset(2021, 3, 30, 11, 14, 3, new TimeSpan(0, 0, 0)).ToOffset(new TimeSpan(13, 0, 0)),
        new DateTimeOffset(2021, 3, 30, 11, 14, 4, new TimeSpan(0, 0, 0)),
        new DateTimeOffset(2021, 3, 30, 11, 14, 5, new TimeSpan(0, 0, 0)).ToOffset(new TimeSpan(13, 0, 0)),
        new DateTimeOffset(2021, 3, 30, 11, 14, 6, new TimeSpan(0, 0, 0)), // Last item in filter
    };

    var dateTimeOffsetsMappedToDatabase = dateTimeOffsets
        .Select(x => codeToDatabase(x))
        .ToList();

    var dateTimeOffsetsMappedToDatabaseFiltered = dateTimeOffsetsMappedToDatabase
        .Where(x => x >= startTime)
        .Where(x => x <= endTime);

    var dateTimeOffsetsMappedBackToCode = dateTimeOffsetsMappedToDatabaseFiltered
        .Select(x => databaseToCode(x))
        .ToList();

    for (var i = 0; i < dateTimeOffsetsMappedBackToCode.Count; i++)
    {
        var difference = dateTimeOffsetsMappedBackToCode[i] - dateTimeOffsetsFilteredExpectations[i];
        Assert.AreEqual(0, difference.TotalMilliseconds);
    }
}
```

This fails. Same data just with some DateTimeOffset objects converted to different timezones.

## What is Happening?

### DifferentTimeZones_DoNotSortWell

The result from DifferentTimeZones_DoNotSortWell in `dateTimeOffsetsMappedBackToCode` is:

```text
[0]	{30/03/2021 11:13:59 AM +00:00}	System.DateTimeOffset
[1]	{30/03/2021 11:14:00 AM +00:00}	System.DateTimeOffset
[2]	{30/03/2021 11:14:02 AM +00:00}	System.DateTimeOffset
[3]	{30/03/2021 11:14:03 AM +00:00}	System.DateTimeOffset
[4]	{30/03/2021 11:14:05 AM +00:00}	System.DateTimeOffset
[5]	{31/03/2021 12:14:01 AM +13:00}	System.DateTimeOffset
[6]	{31/03/2021 12:14:04 AM +13:00}	System.DateTimeOffset
```

We can see that our +1300 DateTimeOffsets have been sorted to the bottom which is not correct.

### DifferentTimeZones_DoNotFilterWell

The result from DifferentTimeZones_DoNotFilterWell in `dateTimeOffsetsMappedBackToCode` is

```text
[0]	{30/03/2021 11:14:02 AM +00:00}	System.DateTimeOffset
[1]	{30/03/2021 11:14:04 AM +00:00}	System.DateTimeOffset
[2]	{30/03/2021 11:14:06 AM +00:00}	System.DateTimeOffset
```

We can see that our +1300 DateTimeOffsets have been completely filtered out which is not correct.

I had more of a play around with this and it happens for much larger gaps than a few seconds - it can happen between hours.

## Why is This Happening?

If we look at the [implementation of DateTimeOffsetToBinaryConverter](https://github.com/dotnet/efcore/blob/main/src/EFCore/Storage/ValueConversion/DateTimeOffsetToBinaryConverter.cs), we can see it uses

```csharp
v => ((v.Ticks / 1000) << 11) | ((long)v.Offset.TotalMinutes & 0x7FF)
```
 
to map DateTimeOffsets to long and
 
```csharp
v => new DateTimeOffset(
    new DateTime((v >> 11) * 1000),
    new TimeSpan(0, (int)((v << 53) >> 53), 0))
```

to map longs back to DateTimeOffset.

Pretty much the ticks of the DateTimeOffset is being stored in the top (MSB) 53 bits and the offset is being turned into minutes and stored in the bottom (LSB) 11 bits.

Here are some mappings:

```text
new DateTimeOffset(2021, 3, 30, 11, 14, 0, new TimeSpan(0, 0, 0))                                    1305655288627200000
new DateTimeOffset(2021, 3, 30, 11, 14, 1, new TimeSpan(0, 0, 0))                                    1305655288647680000
new DateTimeOffset(2021, 3, 30, 11, 14, 1, new TimeSpan(0, 0, 0)).ToOffset(new TimeSpan(13, 0, 0))   1305656247111680780
```

So `new DateTimeOffset(2021, 3, 30, 11, 14, 1, new TimeSpan(0, 0, 0)) == new DateTimeOffset(2021, 3, 30, 11, 14, 1, new TimeSpan(0, 0, 0)).ToOffset(new TimeSpan(13, 0, 0))` is `true` but we would not expect their values to be the same above as they are storing timezones.

We would however expect to see the first 53 bits the same, but when looking at the bits in the DateTimeOffsetToBinaryConverter conversion:

```text
1305655288647680000 => 00010010000111101001111010010001001111101111010010000 00000000000
1305656247111680780 => 00010010000111101001111101110000011001111101110010000 01100001100
```

We can see those first 53 bits are not the same. Whaaaaaat.

The docs for [DateTimeOffset.Ticks](https://docs.microsoft.com/en-us/dotnet/api/system.datetimeoffset.ticks?view=net-5.0) say:

> The Ticks property is not affected by the value of the Offset property.
>
> The value of the Ticks property represents the number of 100-nanosecond intervals that have elapsed since 12:00:00 midnight on January 1, 0001 (the value of MinValue).

But why do we have [DateTimeOffset.UtcTicks](https://docs.microsoft.com/en-us/dotnet/api/system.datetimeoffset.utcticks?view=net-5.0) then?

> The value of the UtcTicks property represents the number of 100-nanosecond intervals that have elapsed since 12:00:00 midnight on January 1, 0001 (the value of MinValue).

Looks like DateTimeOffsetToBinaryConverter should be using UtcTicks and reconstructing the DateTimeOffset object with something that supports this.

Now even if this did work, it would only fix the sorting part of the problem. This is because the filter would still drop anything with a positive timezone as its value would be greater than the converted long value for a given time (assuming the filtering time is in UTC). 


## The Fix I Implemented

So what did I do? I ditched the timezone. I don't need it, I just use DateTimeOffset objects to be safer.

My new converter:

```csharp
using Microsoft.EntityFrameworkCore.Storage.ValueConversion;
using System;

namespace Server.Api.Database
{

    /// <summary>
    ///     Converts <see cref="DateTimeOffset" /> to and from a long representing UTC DateTime ticks.
    /// </summary>
    /// <remarks>
    ///     Check this out to view it in SQL: https://stackoverflow.com/questions/5855299/how-do-i-display-the-following-in-a-readable-datetime-format
    /// </remarks>
    public class DateTimeOffsetToUtcDateTimeTicksConverter : ValueConverter<DateTimeOffset, long>
    {
        /// <summary>
        ///     Creates a new instance of this converter.
        /// </summary>
        /// <param name="mappingHints">
        ///     Hints that can be used by the <see cref="ITypeMappingSource" /> to create data types with appropriate
        ///     facets for the converted data.
        /// </param>
        public DateTimeOffsetToUtcDateTimeTicksConverter(ConverterMappingHints? mappingHints = null)
            : base(
                v => v.UtcDateTime.Ticks,
                v => new DateTimeOffset(v, new TimeSpan(0, 0, 0)),
                mappingHints)
        {
        }

        /// <summary>
        ///     A <see cref="ValueConverterInfo" /> for the default use of this converter.
        /// </summary>
        public static ValueConverterInfo DefaultInfo { get; }
            = new(typeof(DateTimeOffset), typeof(long), i => new DateTimeOffsetToUtcDateTimeTicksConverter(i.MappingHints));
    }
}
```

And to use it in ContextSetup.cs, a simple swap of the converter:

```csharp
foreach (var property in properties)
{
    modelBuilder
        .Entity(entityType.Name)
        .Property(property.Name)
        .HasConversion(new DateTimeOffsetToUtcDateTimeTicksConverter()); // I only changed this
}
```

Pretty much DateTimeOffsetToUtcDateTimeTicksConverter just converts the DateTimeOffset object to a UTC date and then gets the ticks, this is then stored in the database. To read it back out, I re-create the DateTimeOffset with a +0000 timezone.

> Warning: You will lose the original timezone

### Migrating Existing Data

Chuck on your sunnies for this one:

```csharp
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Migrations;
using System;
using System.Collections.Generic;
using System.Linq;

namespace Server.Api.Database.Migrations
{
    public partial class MigrateToDateTimeOffsetToUtcDateTimeTicksConverter : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            foreach (var (Name, DateTimeOffsetProperties) in GetAllDateTimeOffsetEntityProperties())
            {
                foreach (var propertyName in DateTimeOffsetProperties)
                {
                    // Reversing the implementation at https://github.com/dotnet/efcore/blob/main/src/EFCore/Storage/ValueConversion/DateTimeOffsetToBinaryConverter.cs and turning these into DateTime.Ticks fields (https://docs.microsoft.com/en-us/dotnet/api/system.datetimeoffset.ticks?view=net-5.0)
                    migrationBuilder.Sql($"UPDATE {Name} SET {propertyName} = (({propertyName} >> 11) * 1000) - ((({propertyName} << 53) >> 53) * 60 * 10000000)");
                }
            }
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            foreach (var (Name, DateTimeOffsetProperties) in GetAllDateTimeOffsetEntityProperties())
            {
                foreach (var propertyName in DateTimeOffsetProperties)
                {
                    // To put them back we can do the opposite but just ignore the timezone as it is already part of the date. Technically still the same time, just a different time zone which we don't really care about.
                    migrationBuilder.Sql($"UPDATE {Name} SET {propertyName} = ({propertyName} / 1000) << 11");
                }
            }
        }

        /// <summary>
        /// Identify all the columns in the database that have a DateTimeOffset or DateTimeOffset? type
        /// </summary>
        /// <returns></returns>
        private static List<(string Name, List<string> DateTimeOffsetProperties)> GetAllDateTimeOffsetEntityProperties()
        {
            var entityTypes = typeof(Context)
                .GetProperties()
                .Where(x => x.PropertyType.IsGenericType && (typeof(DbSet<>).IsAssignableFrom(x.PropertyType.GetGenericTypeDefinition())))
                .Select(x => (
                    Name: x.Name,
                    DateTimeOffsetProperties: x.PropertyType.GetGenericArguments()[0]
                        .GetProperties()
                        .Where(p => p.PropertyType == typeof(DateTimeOffset) || p.PropertyType == typeof(DateTimeOffset?))
                        .Select(x => x.Name)
                        .ToList()))
                .ToList();

            return entityTypes;
        }
    }
}
```

Boy was that math fun, and it gave me a chance to get a bit dirty with C# reflection again!

## The Trade-Off

There is a trade-off we are seeing here: either have timezones stored and not be able to filter correctly or don't store timezones and use DateTimeOffset to simply be safer with times.

I have used DateTimeOffset so when clients send a time in a different timezone, I don't need to worry and the framework will handle it - this will not happen automatically with DateTime objects.

I understand some people will want to keep the original timezone but it may be a better option to store this in a different column.
