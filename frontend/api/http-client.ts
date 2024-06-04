/* eslint-disable */
/* tslint:disable */
/*
 * ---------------------------------------------------------------
 * ## THIS FILE WAS GENERATED VIA SWAGGER-TYPESCRIPT-API        ##
 * ##                                                           ##
 * ## AUTHOR: acacode                                           ##
 * ## SOURCE: https://github.com/acacode/swagger-typescript-api ##
 * ---------------------------------------------------------------
 */

export const createFormData = (
  object: Record<string, string | File | File[]>,
) => {
  const formData = new FormData();

  Object.keys(object).forEach((key) => {
    const value = object[key];
    if (Array.isArray(value)) {
      value.forEach((file) => formData.append(key, file));
    } else {
      formData.append(key, value);
    }
  });

  return formData;
};
