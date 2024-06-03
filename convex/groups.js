import { mutation } from "./_generated/server";
import { v } from "convex/values";

export const getById = mutation({
  args: {
    id: v.id("updated_groups")
  },
  handler: async (ctx, args) => {
    return await ctx.db.query("updated_groups")
      .filter(q => q.eq(q.field("_id"), args.id))
      .collect();
  },
});

export const createGroups = mutation({
  args: {
    'name': v.string(),
    'description': v.string(),
    'is_public': v.boolean(),
    'organization_id': v.optional(v.id("updated_organizations"))
  },
  handler: async (ctx, args) => {
    let result;
    if(args.organization_id)
      result = await ctx.db
        .insert("updated_groups", {
          name: args.name,
          description: args.description,
          is_public: args.is_public,
          organization_id: args.organization_id
        });
    else
      result = await ctx.db
        .insert("updated_groups", {
          name: args.name,
          description: args.description,
          is_public: args.is_public
        })
    return { success: true, result };
  }
})

export const updateGroups = mutation({
  args: {
    id: v.id("updated_groups"),
    name: v.string(),
    description: v.string(),
    is_public: v.boolean(),
    organization_id: v.optional(v.id("updated_organizations"))
  },
  handler: async (ctx, args) => {
    try {
      if(args.organization_id)
        await ctx.db.patch(args.id, {
          name: args.name,
          description: args.description,
          is_public: args.is_public,
          organization_id: args.organization_id
        });
      else
        await ctx.db.patch(args.id, {
          name: args.name,
          description: args.description,
          is_public: args.is_public
        });
      return { success: true, result: args.id };
    } catch(e) {
      return { success: false, result: "Failed to update a group"}
    }
  },
});

export const deleteGroups = mutation({
  args: {
    id: v.id("updated_groups")
  },
  handler: async (ctx, args) => {
    return await ctx.db.delete(args.id);
  }
})