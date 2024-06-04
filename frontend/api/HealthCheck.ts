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

import { AxiosError } from "axios";
import useSWR, { SWRConfiguration } from "swr";

/**
 * Health check endpoint to verify that the API is up and running.
 */
export const useHealthCheck = (config?: SWRConfiguration<string>) => {
  return useSWR<string, AxiosError>(`/health-check`, config);
};
