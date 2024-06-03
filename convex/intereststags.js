import { query, mutation } from "./_generated/server";
import { v } from "convex/values";

export const get = query({
  handler: async (ctx) => {
    return await ctx.db.query("updated_intereststags").collect();
  },
});

export const insertInterestsTags = mutation({
  args: {
    name: v.string(),
  },
  handler: async (ctx, args) => {
    let result = await ctx.db
      .insert("updated_intereststags", {
        name: args.name
      });
    if (result) {
      return { success: true, result };
    } else {
      return { success: false, result: "Failed to insert interests tag." };
    }
  },
});

export const updateInterestsTags = mutation({
  args: {
    name: v.string(),
    id: v.id("updated_intereststags")
  },
  handler: async (ctx, args) => {
    await ctx.db.patch(args.id, {
      name: args.name
    });
    let result = args.id;
    if (result) {
      return { success: true, result };
    } else {
      return { success: false, result: "Failed to update interests tag." };
    }
  },
});

export const deleteInterestsTags = mutation({
  args: {
    id: v.id("updated_intereststags")
  },
  handler: async (ctx, args) => {
    await ctx.db.delete(args.id);
    return { success: true, result: "Deleted InterestsTag Successfully" };
  },
});