import { mutation } from "./_generated/server";
import { v } from "convex/values";

export const getById = mutation({
  args: {
    id: v.id("updated_organizations")
  },
  handler: async (ctx, args) => {
    return await ctx.db.query("updated_organizations")
      .filter(q => q.eq(q.field("_id"), args.id))
      .collect();
  },
});