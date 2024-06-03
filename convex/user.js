import { mutation, } from "./_generated/server";
import { v } from "convex/values";

export const getById = mutation({
    args: {
        id: v.id("updated_users")
    },
    handler: async (ctx, args) => {
        const result = await ctx.db.query("updated_users")
            .filter(q => q.eq(q.field("_id"), args.id))
            .unique();

        if (result) {
            return { success: true, result };
        } else {
            return { success: false, result: null };
        }
    },
});

export const getUserByUsername = mutation({
    args: {
        username: v.string()
    },
    handler: async (ctx, args) => {
        const result = await ctx.db.query("updated_users")
            .filter(q => q.eq(q.field("username"), args.username))
            .first();

        if (result) {
            return { success: true, result };
        } else {
            return { success: false, result: null };
        }
    },
});

export const getUserByEmail = mutation({
    args: {
        email: v.string()
    },
    handler: async (ctx, args) => {
        const result = await ctx.db.query("updated_users")
            .filter(q => q.eq(q.field("email"), args.email))
            .first();

        if (result) {
            return { success: true, result };
        } else {
            return { success: false, result: "Failed to update or insert profile." };
        }
    },
});

export const createUser = mutation({
    args: {
        email: v.string(),
        password: v.string(),
        username: v.string(),
        first_name: v.string(),
        last_name: v.string(),
    },
    handler: async (ctx, args) => {
        const user = {
            email: args.email,
            password: args.password, // Ensure the password is hashed before storing
            username: args.username,
            first_name: args.first_name || '',
            last_name: args.last_name || '',
            is_active: args.is_active || false,
            last_joined_at: new Date().toISOString(),
        };
        const result = await ctx.db.insert('updated_users', user);

        if (result) {
            return { success: true, result };
        } else {
            return { success: false, result: "Failed to update or insert profile." };
        }
    },
});

export const updateUser = mutation({
    args: {
        first_name: v.string(),
        last_name: v.string(),
        user_id: v.id("updated_users"),
    },
    handler: async (ctx, args) => {
        await ctx.db.patch(args.user_id, {
            first_name: args.first_name,
            second_name: args.second_name
        });
        return { success: true, result: args.user_id };
    },
});

export const activateOrDeactivateUser = mutation({
    args: {
        is_active: v.boolean(),
        user_id: v.id("updated_users"),
    },
    handler: async (ctx, args) => {
        await ctx.db.patch(args.user_id, {
            is_active: args.is_active
        });
        return { success: true, result: args.user_id };
    },
});

export const updateUserEmail = mutation({
    args: {
        email: v.string(),
        user_id: v.id("updated_users"),
    },
    handler: async (ctx, args) => {
        await ctx.db.patch(args.user_id, {
            email: args.email
        });
        return { success: true, result: args.user_id };
    },
});

export const updateUserPassword = mutation({
    args: {
        password: v.string(),
        user_id: v.id("updated_users"),
    },
    handler: async (ctx, args) => {
        await ctx.db.patch(args.user_id, {
            password: args.password
        });
        return { success: true, result: args.user_id };
    },
});