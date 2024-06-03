import { mutation } from "./_generated/server";
import { v } from "convex/values";

export const getById = mutation({
    args: {
        id: v.id("updated_usernewemails")
    },
    handler: async (ctx, args) => {
        return await ctx.db.query("updated_usernewemails")
            .filter(q => q.eq(q.field("_id"), args.id))
            .collect();
    },
});

export const getByUserId = mutation({
    args: {
        user_id: v.id("updated_users")
    },
    handler: async (ctx, args) => {
        let result = await ctx.db.query("updated_usernewemails")
            .filter(q => q.eq(q.field("user_id"), args.user_id))
            .unique();

        if (result) {
            return { success: true, result };
        } else {
            return { success: false, result: "Failed to fetch email." };
        }
    },
});

export const insertNewEmail = mutation({
    args: {
        new_email: v.string(),
        user_id: v.id("updated_users"),
    },
    handler: async (ctx, args) => {
        let result;

        const exist_user_profile = await ctx.db
            .query("updated_usernewemails")
            .filter(q => q.eq(q.field("user_id"), args.user_id))
            .collect();
        const id = exist_user_profile[0]?._id;
        if (id) {
            await ctx.db.patch(id, {
                new_email: args.new_email
            });
            result = id;
        } else {
            result = await ctx.db
                .insert("updated_usernewemails", {
                    new_email: args.new_email,
                    user_id: args.user_id
                });
        }

        if (result) {
            return { success: true, result };
        } else {
            return { success: false, result: "Failed to update or insert token." };
        }
    },
});

export const deleteUserEmailById = mutation({
    args: {
        id: v.id("updated_usernewemails")
    },
    handler: async (ctx, args) => {
        await ctx.db.delete(args.id);
        return { success: true, result: args.id };
    },
});